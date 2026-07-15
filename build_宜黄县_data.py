#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 宜黄县 (抚州市, 江西省) leadership network.

Data sourced from 宜黄县人民政府网站 (www.jxyh.gov.cn), leadership pages,
news articles, and meeting reports. Where information is incomplete, it is marked
with explicit confidence levels.

宜黄县概况: 宜黄县是江西省抚州市下辖的一个县，位于江西省中部偏东，抚州市南部。
面积约1944平方公里，人口约24万。下辖6镇6乡。
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_宜黄县")
DB_PATH = os.path.join(STAGING, "宜黄县_network.db")
GEXF_PATH = os.path.join(STAGING, "宜黄县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# DATA
# =========================================================================

# ── Notes on Data Sources ──
# 1. 杜晓良 biography: https://www.jxyh.gov.cn/col/col28258/index.html (2026-07)
# 2. 曾祥清 biography: https://www.jxyh.gov.cn/col/col28596/index.html (2026-07)
# 3. 李娜 biography: https://www.jxyh.gov.cn/col/col28260/index.html (2026-07)
# 4. Leadership page: https://www.jxyh.gov.cn/col/col1975/index.html
# 5. Transition news (杜晓良 to 王峰): https://www.jxyh.gov.cn/art/2026/7/9/art_1994_4460534.html (2026-07-07: 王峰 as 县委书记, 曾祥清 as 县长候选人)
# 6. 陈小青 last appearance as 县长: https://www.jxyh.gov.cn/art/2026/6/24/art_2097_4456529.html (2026-06-23)
# 7. 杜晓良 last appearance as 县委书记: https://www.jxyh.gov.cn/art/2026/6/30/art_1994_4458048.html (2026-06-29)
# 8. 王峰 first appearance as 县委书记: https://www.jxyh.gov.cn/art/2026/7/9/art_1994_4460534.html (2026-07-07)
# 9. 王峰 first news as 县委书记: https://www.jxyh.gov.cn/art/2026/7/13/art_1994_4461162.html (2026-07-11)

persons = [
    # ── Core Leaders: Current Party Secretary ──
    {
        "id": 1,
        "name": "王峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县委书记",
        "current_org": "中共宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/art/2026/7/9/art_1994_4460534.html — 宜黄县政府新闻（2026年7月7日，王峰以县委书记身份出席全县政绩观学习教育调度会）"
    },

    # ── Core Leaders: Previous Party Secretary ──
    {
        "id": 2,
        "name": "杜晓良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-12",
        "birthplace": "江西广昌",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1989-08",
        "current_post": "宜黄县委书记（前任）",
        "current_org": "中共宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/col/col28258/index.html — 宜黄县政府网站领导专页"
    },

    # ── Core Leaders: Current County Mayor ──
    {
        "id": 3,
        "name": "曾祥清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-06",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县委副书记、县长",
        "current_org": "宜黄县人民政府",
        "source": "https://www.jxyh.gov.cn/col/col28596/index.html — 宜黄县政府网站领导专页"
    },

    # ── Core Leaders: Previous County Mayor ──
    {
        "id": 4,
        "name": "陈小青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县委副书记、县长（前任）",
        "current_org": "宜黄县人民政府",
        "source": "https://www.jxyh.gov.cn/art/2026/6/24/art_2097_4456529.html — 宜黄县政府新闻（2026年6月23日，陈小青以县长身份调研）"
    },

    # ── County Leaders: Deputy Party Secretary ──
    {
        "id": 5,
        "name": "李娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-06",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县委副书记",
        "current_org": "中共宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/col/col28260/index.html — 宜黄县政府网站领导专页"
    },

    # ── County Leaders: Party Standing Committee ──
    {
        "id": 6,
        "name": "李坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-11",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县委常委、政法委书记",
        "current_org": "中共宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/col/col28261/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 7,
        "name": "杨磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-11",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县委常委、统战部部长",
        "current_org": "中共宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/col/col28262/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 8,
        "name": "周钦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-08",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县委常委、常务副县长",
        "current_org": "宜黄县人民政府",
        "source": "https://www.jxyh.gov.cn/col/col28263/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 9,
        "name": "邹锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-02",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县委常委、副县长，县工业园区党工委书记",
        "current_org": "宜黄县人民政府",
        "source": "https://www.jxyh.gov.cn/col/col28264/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 10,
        "name": "苏余森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-02",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县委常委、县人武部部长",
        "current_org": "宜黄县人民武装部",
        "source": "https://www.jxyh.gov.cn/col/col28265/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 11,
        "name": "尹续平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-02",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县委常委、组织部部长",
        "current_org": "中共宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/col/col28266/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 12,
        "name": "于志云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-11",
        "birthplace": "",
        "education": "大学专科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县委常委、县纪委书记、县监委主任",
        "current_org": "中共宜黄县纪律检查委员会",
        "source": "https://www.jxyh.gov.cn/col/col28267/index.html — 宜黄县政府网站领导专页"
    },

    # ── County Government: Deputy Mayors ──
    {
        "id": 13,
        "name": "邵明申",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-03",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "宜黄县人民政府副县长",
        "current_org": "宜黄县人民政府",
        "source": "https://www.jxyh.gov.cn/col/col28277/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 14,
        "name": "胡海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-08",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县人民政府副县长",
        "current_org": "宜黄县人民政府",
        "source": "https://www.jxyh.gov.cn/col/col28278/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 15,
        "name": "罗小刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "宜黄县人民政府副县长",
        "current_org": "宜黄县人民政府",
        "source": "https://www.jxyh.gov.cn/col/col28279/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 16,
        "name": "杨抚平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-07",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县人民政府副县长",
        "current_org": "宜黄县人民政府",
        "source": "https://www.jxyh.gov.cn/col/col28275/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 17,
        "name": "吴媚",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986-07",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县人民政府副县长",
        "current_org": "宜黄县人民政府",
        "source": "https://www.jxyh.gov.cn/col/col28280/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 18,
        "name": "欧阳普华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-03",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县人民政府副县长",
        "current_org": "宜黄县人民政府",
        "source": "https://www.jxyh.gov.cn/col/col28281/index.html — 宜黄县政府网站领导专页"
    },

    # ── People's Congress ──
    {
        "id": 19,
        "name": "许甘泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-09",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县人大常委会主任",
        "current_org": "宜黄县人民代表大会常务委员会",
        "source": "https://www.jxyh.gov.cn/col/col28268/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 20,
        "name": "黄小勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县人大常委会副主任",
        "current_org": "宜黄县人民代表大会常务委员会",
        "source": "https://www.jxyh.gov.cn/col/col28269/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 21,
        "name": "黄双龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "宜黄县人大常委会副主任",
        "current_org": "宜黄县人民代表大会常务委员会",
        "source": "https://www.jxyh.gov.cn/col/col28270/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 22,
        "name": "江志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-03",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县人大常委会副主任",
        "current_org": "宜黄县人民代表大会常务委员会",
        "source": "https://www.jxyh.gov.cn/col/col28271/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 23,
        "name": "邵建宜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜黄县人大常委会副主任",
        "current_org": "宜黄县人民代表大会常务委员会",
        "source": "https://www.jxyh.gov.cn/col/col1975/index.html — 宜黄县政府网站领导页面"
    },

    # ── CPPCC ──
    {
        "id": 24,
        "name": "高志坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜黄县政协主席",
        "current_org": "中国人民政治协商会议宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/col/col28282/index.html — 宜黄县政府网站领导专页"
    },
    {
        "id": 25,
        "name": "彭武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜黄县政协副主席",
        "current_org": "中国人民政治协商会议宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/col/col1975/index.html — 宜黄县政府网站领导页面"
    },
    {
        "id": 26,
        "name": "冯志榕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜黄县政协副主席",
        "current_org": "中国人民政治协商会议宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/col/col1975/index.html — 宜黄县政府网站领导页面"
    },
    {
        "id": 27,
        "name": "曹佳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜黄县政协副主席",
        "current_org": "中国人民政治协商会议宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/col/col1975/index.html — 宜黄县政府网站领导页面"
    },
    {
        "id": 28,
        "name": "陈荣林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜黄县政协副主席",
        "current_org": "中国人民政治协商会议宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/col/col1975/index.html — 宜黄县政府网站领导页面"
    },
    {
        "id": 29,
        "name": "黄建鸿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜黄县政协副主席",
        "current_org": "中国人民政治协商会议宜黄县委员会",
        "source": "https://www.jxyh.gov.cn/col/col1975/index.html — 宜黄县政府网站领导页面"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共宜黄县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共抚州市委员会",
        "location": "宜黄县"
    },
    {
        "id": 2,
        "name": "宜黄县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "抚州市人民政府",
        "location": "宜黄县"
    },
    {
        "id": 3,
        "name": "宜黄县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "宜黄县",
        "location": "宜黄县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议宜黄县委员会",
        "type": "政协",
        "level": "县",
        "parent": "宜黄县",
        "location": "宜黄县"
    },
    {
        "id": 5,
        "name": "中共宜黄县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共宜黄县委员会",
        "location": "宜黄县"
    },
    {
        "id": 6,
        "name": "宜黄县人民武装部",
        "type": "政府",
        "level": "县",
        "parent": "抚州军分区",
        "location": "宜黄县"
    },
    {
        "id": 7,
        "name": "宜黄县工业园区",
        "type": "开发区",
        "level": "县",
        "parent": "宜黄县人民政府",
        "location": "宜黄县"
    },
]

positions = [
    # ── 王峰 ──
    {"person_id": 1, "org_id": 1, "title": "宜黄县委书记", "start": "2026-07", "end": "", "rank": "正处级", "note": "2026年7月初到任，接替杜晓良"},
    # ── 杜晓良 ──
    {"person_id": 2, "org_id": 1, "title": "宜黄县委书记", "start": "", "end": "2026-06", "rank": "正处级", "note": "前任县委书记，2026年6月30日仍以县委书记身份出席活动"},
    # ── 曾祥清 ──
    {"person_id": 3, "org_id": 2, "title": "宜黄县县长", "start": "2026-07", "end": "", "rank": "正处级", "note": "2026年7月7日以县长候选人身份主持会议，后确认任职"},
    {"person_id": 3, "org_id": 1, "title": "宜黄县委副书记", "start": "", "end": "", "rank": "副处级", "note": "兼任县委副书记"},
    # ── 陈小青 ──
    {"person_id": 4, "org_id": 2, "title": "宜黄县县长（前任）", "start": "", "end": "2026-06", "rank": "正处级", "note": "2026年6月23日仍以县长身份调研"},
    {"person_id": 4, "org_id": 1, "title": "宜黄县委副书记（前任）", "start": "", "end": "2026-06", "rank": "副处级", "note": "前任县委副书记、县长"},
    # ── 李娜 ──
    {"person_id": 5, "org_id": 1, "title": "宜黄县委副书记", "start": "", "end": "", "rank": "副处级", "note": "协助县委书记处理县委日常工作"},
    # ── 李坚 ──
    {"person_id": 6, "org_id": 1, "title": "宜黄县委常委、政法委书记", "start": "", "end": "", "rank": "副处级", "note": "负责政法、信访维稳工作"},
    # ── 杨磊 ──
    {"person_id": 7, "org_id": 1, "title": "宜黄县委常委、统战部部长", "start": "", "end": "", "rank": "副处级", "note": "负责统一战线工作"},
    # ── 周钦 ──
    {"person_id": 8, "org_id": 2, "title": "宜黄县委常委、常务副县长", "start": "", "end": "", "rank": "副处级", "note": "协助县长分管县政府常务工作"},
    {"person_id": 8, "org_id": 1, "title": "宜黄县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    # ── 邹锋 ──
    {"person_id": 9, "org_id": 2, "title": "宜黄县副县长", "start": "", "end": "", "rank": "副处级", "note": "在外挂职，暂不分工"},
    {"person_id": 9, "org_id": 7, "title": "宜黄县工业园区党工委书记", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "宜黄县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    # ── 苏余森 ──
    {"person_id": 10, "org_id": 6, "title": "宜黄县人武部部长", "start": "", "end": "", "rank": "正团级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "宜黄县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    # ── 尹续平 ──
    {"person_id": 11, "org_id": 1, "title": "宜黄县委常委、组织部部长", "start": "", "end": "", "rank": "副处级", "note": "负责党的建设和组织工作"},
    # ── 于志云 ──
    {"person_id": 12, "org_id": 5, "title": "宜黄县纪委书记、县监委主任", "start": "", "end": "", "rank": "副处级", "note": "负责纪律检查和监察工作"},
    {"person_id": 12, "org_id": 1, "title": "宜黄县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    # ── 邵明申 ──
    {"person_id": 13, "org_id": 2, "title": "宜黄县副县长", "start": "", "end": "", "rank": "副处级", "note": "负责司法、文化旅游等工作"},
    # ── 胡海 ──
    {"person_id": 14, "org_id": 2, "title": "宜黄县副县长", "start": "", "end": "", "rank": "副处级", "note": "负责公安工作"},
    # ── 罗小刚 ──
    {"person_id": 15, "org_id": 2, "title": "宜黄县副县长", "start": "", "end": "", "rank": "副处级", "note": "负责教育、体育、卫健等工作；无党派"},
    # ── 杨抚平 ──
    {"person_id": 16, "org_id": 2, "title": "宜黄县副县长", "start": "", "end": "", "rank": "副处级", "note": "负责住建、城管、自然资源等工作"},
    # ── 吴媚 ──
    {"person_id": 17, "org_id": 2, "title": "宜黄县副县长", "start": "", "end": "", "rank": "副处级", "note": "负责工业、商务、市场监管等工作"},
    # ── 欧阳普华 ──
    {"person_id": 18, "org_id": 2, "title": "宜黄县副县长", "start": "", "end": "", "rank": "副处级", "note": "负责农业农村、林业、水利等工作"},
    # ── 人大 ──
    {"person_id": 19, "org_id": 3, "title": "宜黄县人大常委会主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "宜黄县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "宜黄县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": "无党派"},
    {"person_id": 22, "org_id": 3, "title": "宜黄县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 3, "title": "宜黄县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    # ── 政协 ──
    {"person_id": 24, "org_id": 4, "title": "宜黄县政协主席", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 25, "org_id": 4, "title": "宜黄县政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 4, "title": "宜黄县政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 27, "org_id": 4, "title": "宜黄县政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 28, "org_id": 4, "title": "宜黄县政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 29, "org_id": 4, "title": "宜黄县政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
]

relationships = [
    # ── Predecessor/Successor: Party Secretary ──
    {
        "person_a": 2, "person_b": 1,
        "type": "predecessor_successor",
        "context": "杜晓良为前任县委书记，王峰于2026年7月初接任",
        "overlap_org": "中共宜黄县委员会",
        "overlap_period": "",
        "confidence": "confirmed"
    },
    # ── Predecessor/Successor: County Mayor ──
    {
        "person_a": 4, "person_b": 3,
        "type": "predecessor_successor",
        "context": "陈小青为前任县长，曾祥清于2026年7月接任",
        "overlap_org": "宜黄县人民政府",
        "overlap_period": "",
        "confidence": "confirmed"
    },
    # ── Overlap: 杜晓良 and 陈小青 ──
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "杜晓良（县委书记）和陈小青（县长）曾在宜黄县共事",
        "overlap_org": "中共宜黄县委员会",
        "overlap_period": "",
        "confidence": "confirmed"
    },
    # ── Overlap: 杜晓良 and 李娜 ──
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "杜晓良任县委书记期间，李娜任县委副书记",
        "overlap_org": "中共宜黄县委员会",
        "overlap_period": "",
        "confidence": "confirmed"
    },
    # ── Overlap: 杜晓良 and 曾祥清 (as deputy secretary) ──
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "杜晓良任县委书记期间，曾祥清一度任县委副书记",
        "overlap_org": "中共宜黄县委员会",
        "overlap_period": "",
        "confidence": "confirmed"
    },
    # ── Overlap: 曾祥清 and 李娜 ──
    {
        "person_a": 3, "person_b": 5,
        "type": "overlap",
        "context": "曾祥清（县委副书记、县长）和李娜（县委副书记）同为县委副书记",
        "overlap_org": "中共宜黄县委员会",
        "overlap_period": "",
        "confidence": "confirmed"
    },
    # ── Overlap: 周钦 and 邹锋 (both young, born 1986) ──
    {
        "person_a": 8, "person_b": 9,
        "type": "overlap",
        "context": "周钦（常务副县长，1986年生）和邹锋（副县长，1986年生）同为80后县领导，在县政府共事",
        "overlap_org": "宜黄县人民政府",
        "overlap_period": "",
        "confidence": "confirmed"
    },
    # ── Overlap: 周钦 and 邹锋 in party committee ──
    {
        "person_a": 8, "person_b": 9,
        "type": "overlap",
        "context": "周钦和邹锋同为县委常委",
        "overlap_org": "中共宜黄县委员会",
        "overlap_period": "",
        "confidence": "confirmed"
    },
    # ── Overlap: All standing committee members ──
    {
        "person_a": 1, "person_b": 8,
        "type": "overlap",
        "context": "王峰（县委书记）和周钦（常务副县长）为县委班子领导",
        "overlap_org": "中共宜黄县委员会",
        "overlap_period": "",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "王峰（县委书记）和李娜（县委副书记）在县委班子共事",
        "overlap_org": "中共宜黄县委员会",
        "overlap_period": "",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 11,
        "type": "overlap",
        "context": "王峰（县委书记）和尹续平（组织部部长）在县委班子共事",
        "overlap_org": "中共宜黄县委员会",
        "overlap_period": "",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 12,
        "type": "overlap",
        "context": "王峰（县委书记）和于志云（纪委书记）在县委班子共事",
        "overlap_org": "中共宜黄县委员会",
        "overlap_period": "",
        "confidence": "confirmed"
    },
]

# =========================================================================
# SQLite
# =========================================================================

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
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
        source TEXT
    );

    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );

    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        org_id INTEGER,
        title TEXT,
        start TEXT,
        "end" TEXT,
        rank TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER,
        person_b INTEGER,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        confidence TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    cur.execute("""
        INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
          p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""
        INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""
        INSERT INTO positions (person_id, org_id, title, start, "end", rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

for r in relationships:
    cur.execute("""
        INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

conn.commit()
conn.close()

print(f"✓ SQLite database written: {DB_PATH}")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")

# =========================================================================
# GEXF
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role and "纪委" not in role and "副书记" not in role:
        return "255,50,50"
    elif "县长" in role:
        return "50,100,255"
    elif "纪委" in role or "监委" in role:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif t == "开发区":
        return "200,255,200"
    elif t == "人大":
        return "200,255,255"
    elif t == "政协":
        return "255,240,200"
    else:
        return "200,200,200"

def is_top_leader(p):
    role = p.get("current_post", "")
    return "县委书记" in role or "县长" in role

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>China Gov Network Research Agent</creator>')
lines.append('    <description>宜黄县领导关系网络 - 宜黄县 (江西省抚州市)</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('      <attribute id="3" title="level" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="label" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append('          <attvalue for="3" value="县处级"/>')
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
    lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# Person-to-organization edges
for pos in positions:
    eid += 1
    p = next(x for x in persons if x["id"] == pos["person_id"])
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Person-to-person relationship edges
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✓ GEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons) + len(organizations)}")
print(f"  Edges: {len(positions) + len(relationships)}")
