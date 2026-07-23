#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
福泉市领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Fuquan City leadership network.

Level: 县级市
Province: 贵州省
Parent City: 黔南布依族苗族自治州
Region: 福泉市
Targets: 市委书记 & 市长

Research Sources:
- www.gzfuquan.gov.cn — 福泉市人民政府门户网站
  - 领导之窗/中共福泉市委: https://www.gzfuquan.gov.cn/zwgk/ldzc/zgfqsw/index.html
  - 领导之窗/市政府: https://www.gzfuquan.gov.cn/zwgk/ldzc/szf/index.html
  - 吴义宁: https://www.gzfuquan.gov.cn/zwgk/ldzc/zgfqsw/202509/t20250902_88554241.html
  - 夏世飞: https://www.gzfuquan.gov.cn/zwgk/ldzc/szf/202305/t20230508_85484559.html
  - 王程远: https://www.gzfuquan.gov.cn/zwgk/ldzc/zgfqsw/202312/t20231211_85484540.html
  - 熊晓龙: https://www.gzfuquan.gov.cn/zwgk/ldzc/srdcwh/202109/t20210918_85484548.html
  - 汪华: https://www.gzfuquan.gov.cn/zwgk/ldzc/szx/202109/t20210916_85484571.html
  - 领导活动/新闻: https://www.gzfuquan.gov.cn/xwzx/ldhd/

Confirmed officeholders (as of 2026-07-23, from www.gzfuquan.gov.cn official leadership pages):

市委领导班子 (10人):
- 吴义宁: 黔南州政协副主席、福泉市委书记、黔南高新区党工委书记 (1972.11, 大学)
- 夏世飞: 福泉市委副书记、市长、市政府党组书记、黔南高新区党工委副书记、管委会主任 (1978.6, 理学博士)
- 王程远: 市委副书记、政法委书记 (1983.7)
- 王楠: 市委常委 (同时任副市长)
- 陈娅: 市委常委 (女)
- 赵泽敏: 市委常委 (同时任副市长)
- 韦超: 市委常委
- 兰娟: 市委常委 (女, 同时任副市长)
- 郭健: 市委常委
- 陈杰: 市委常委

市政府 (1正8副):
- 夏世飞: 市长
- 王楠: 副市长
- 赵泽敏: 副市长
- 兰娟: 副市长
- 徐稳: 副市长
- 付裕: 副市长
- 高建平: 副市长
- 杨炳滔: 副市长
- 赵远彬: 副市长

市人大常委会:
- 熊晓龙: 主任 (1973.12, 省委党校大学)
- 杨绍荣, 周启华, 何平湘, 金志红, 李万江, 王进

市政协:
- 汪华: 主席 (1969.1, 省委党校大学, 女)
- 李毅, 彭建华, 姜天武, 张泉, 陈培银, 刘玉梅

Research Date: 2026-07-23
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (staging mode) ──
SLUG = "福泉市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导班子 (Current CPC Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "吴义宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔南州政协副主席、福泉市委书记、黔南高新技术产业开发区党工委书记",
        "current_org": "中共福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/zgfqsw/202509/t20250902_88554241.html — 官方领导简历"
    },
    {
        "id": 2,
        "name": "夏世飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年6月",
        "birthplace": "",
        "education": "全日制研究生/理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市委副书记、市长、市政府党组书记、黔南高新技术产业开发区党工委副书记、管委会主任",
        "current_org": "福泉市人民政府",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szf/202305/t20230508_85484559.html — 官方领导简历"
    },
    {
        "id": 3,
        "name": "王程远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年7月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市委副书记、政法委书记",
        "current_org": "中共福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/zgfqsw/202312/t20231211_85484540.html — 官方领导简历"
    },
    {
        "id": 4,
        "name": "王楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市委常委、副市长",
        "current_org": "福泉市人民政府",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szf/202512/t20251229_89100324.html — 市政府领导页"
    },
    {
        "id": 5,
        "name": "陈娅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市委常委",
        "current_org": "中共福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/zgfqsw/202311/t20231106_85484539.html — 官方领导页"
    },
    {
        "id": 6,
        "name": "赵泽敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市委常委、副市长",
        "current_org": "福泉市人民政府",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szf/202510/t20251031_88892665.html — 市政府领导页"
    },
    {
        "id": 7,
        "name": "韦超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市委常委",
        "current_org": "中共福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/zgfqsw/202312/t20231211_85484541.html — 官方领导页"
    },
    {
        "id": 8,
        "name": "兰娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市委常委、副市长",
        "current_org": "福泉市人民政府",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szf/202111/t20211103_85484551.html — 市政府领导页"
    },
    {
        "id": 9,
        "name": "郭健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市委常委",
        "current_org": "中共福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/zgfqsw/202504/t20250425_87581669.html — 官方领导页"
    },
    {
        "id": 10,
        "name": "陈杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市委常委",
        "current_org": "中共福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/zgfqsw/202508/t20250812_88449036.html — 官方领导页"
    },
    # ════════════════════════════════════════
    # 市政府班子 (Government — other members)
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "徐稳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市副市长",
        "current_org": "福泉市人民政府",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szf/202408/t20240816_85484567.html — 市政府领导页"
    },
    {
        "id": 12,
        "name": "付裕",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市副市长",
        "current_org": "福泉市人民政府",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szf/202103/t20210317_85484550.html — 市政府领导页"
    },
    {
        "id": 13,
        "name": "高建平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市副市长",
        "current_org": "福泉市人民政府",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szf/202112/t20211227_85484558.html — 市政府领导页"
    },
    {
        "id": 14,
        "name": "杨炳滔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市副市长",
        "current_org": "福泉市人民政府",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szf/202311/t20231106_85484561.html — 市政府领导页"
    },
    {
        "id": 15,
        "name": "赵远彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市副市长",
        "current_org": "福泉市人民政府",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szf/202503/t20250318_87198922.html — 市政府领导页"
    },
    # ════════════════════════════════════════
    # 市人大常委会
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "熊晓龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市人大常委会党组书记、主任",
        "current_org": "福泉市人民代表大会常务委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/srdcwh/202109/t20210918_85484548.html — 官方领导简历"
    },
    {
        "id": 17,
        "name": "杨绍荣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市人大常委会副主任",
        "current_org": "福泉市人民代表大会常务委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/srdcwh/ — 市人大领导页"
    },
    {
        "id": 18,
        "name": "周启华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市人大常委会副主任",
        "current_org": "福泉市人民代表大会常务委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/srdcwh/ — 市人大领导页"
    },
    {
        "id": 19,
        "name": "何平湘",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市人大常委会副主任",
        "current_org": "福泉市人民代表大会常务委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/srdcwh/ — 市人大领导页"
    },
    {
        "id": 20,
        "name": "金志红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市人大常委会副主任",
        "current_org": "福泉市人民代表大会常务委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/srdcwh/ — 市人大领导页"
    },
    {
        "id": 21,
        "name": "李万江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市人大常委会副主任",
        "current_org": "福泉市人民代表大会常务委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/srdcwh/ — 市人大领导页"
    },
    {
        "id": 22,
        "name": "王进",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市人大常委会副主任",
        "current_org": "福泉市人民代表大会常务委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/srdcwh/ — 市人大领导页"
    },
    # ════════════════════════════════════════
    # 市政协
    # ════════════════════════════════════════
    {
        "id": 23,
        "name": "汪华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年1月",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市政协党组书记、主席",
        "current_org": "中国人民政治协商会议福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szx/202109/t20210916_85484571.html — 官方领导简历"
    },
    {
        "id": 24,
        "name": "李毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市政协副主席",
        "current_org": "中国人民政治协商会议福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szx/ — 市政协领导页"
    },
    {
        "id": 25,
        "name": "彭建华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市政协副主席",
        "current_org": "中国人民政治协商会议福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szx/ — 市政协领导页"
    },
    {
        "id": 26,
        "name": "姜天武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市政协副主席",
        "current_org": "中国人民政治协商会议福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szx/ — 市政协领导页"
    },
    {
        "id": 27,
        "name": "张泉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市政协副主席",
        "current_org": "中国人民政治协商会议福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szx/ — 市政协领导页"
    },
    {
        "id": 28,
        "name": "陈培银",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市政协副主席",
        "current_org": "中国人民政治协商会议福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szx/ — 市政协领导页"
    },
    {
        "id": 29,
        "name": "刘玉梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福泉市政协副主席",
        "current_org": "中国人民政治协商会议福泉市委员会",
        "source": "https://www.gzfuquan.gov.cn/zwgk/ldzc/szx/ — 市政协领导页"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共福泉市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共黔南布依族苗族自治州委员会",
        "location": "贵州省黔南布依族苗族自治州福泉市"
    },
    {
        "id": 2,
        "name": "福泉市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "黔南布依族苗族自治州人民政府",
        "location": "贵州省黔南布依族苗族自治州福泉市"
    },
    {
        "id": 3,
        "name": "福泉市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级市",
        "parent": "黔南布依族苗族自治州人民代表大会常务委员会",
        "location": "贵州省黔南布依族苗族自治州福泉市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议福泉市委员会",
        "type": "政协",
        "level": "县级市",
        "parent": "中国人民政治协商会议黔南布依族苗族自治州委员会",
        "location": "贵州省黔南布依族苗族自治州福泉市"
    },
    {
        "id": 5,
        "name": "黔南高新技术产业开发区管理委员会",
        "type": "开发区",
        "level": "县级市",
        "parent": "福泉市人民政府",
        "location": "贵州省黔南布依族苗族自治州福泉市"
    },
    {
        "id": 6,
        "name": "黔南布依族苗族自治州政协",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议贵州省委员会",
        "location": "贵州省黔南布依族苗族自治州都匀市"
    },
]

# 3. Positions
positions = [
    # 吴义宁
    {"person_id": 1, "org_id": 1, "title": "福泉市委书记", "start": "", "end": "present", "rank": "副厅级", "note": "同时兼任黔南州政协副主席（副厅级）"},
    {"person_id": 1, "org_id": 5, "title": "黔南高新技术产业开发区党工委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "黔南州政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": "2025年9月官网确认"},
    # 夏世飞
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长、市政府党组书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 5, "title": "黔南高新区党工委副书记、管委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 王程远
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": "三级调研员"},
    # 市委常委兼副市长
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "同时任副市长"},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "同时任副市长"},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "同时任副市长"},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 市委常委（专职）
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 副市长（专职）
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 市人大常委会
    {"person_id": 16, "org_id": 3, "title": "市人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 市政协
    {"person_id": 23, "org_id": 4, "title": "市政协党组书记、主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 27, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 28, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 29, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# 4. Relationships
relationships = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与市长，党政主要领导搭档",
     "overlap_org": "中共福泉市委员会/福泉市人民政府", "overlap_period": "2023-2026年"},
    # 市委书记 & 副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委书记与市委副书记、政法委书记",
     "overlap_org": "中共福泉市委常委会", "overlap_period": "2023-2026年"},
    # 市委书记 & 市委常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "市委书记与市委常委", "overlap_org": "中共福泉市委常委会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "市委书记与市委常委", "overlap_org": "中共福泉市委常委会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "市委书记与市委常委", "overlap_org": "中共福泉市委常委会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "市委书记与市委常委", "overlap_org": "中共福泉市委常委会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "市委书记与市委常委", "overlap_org": "中共福泉市委常委会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "市委书记与市委常委", "overlap_org": "中共福泉市委常委会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "市委书记与市委常委", "overlap_org": "中共福泉市委常委会", "overlap_period": "2026年"},
    # 市长 & 副市长们
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "市长与副市长（市委常委兼任）", "overlap_org": "福泉市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "市长与副市长（市委常委兼任）", "overlap_org": "福泉市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "市长与副市长（市委常委兼任）", "overlap_org": "福泉市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "市长与副市长", "overlap_org": "福泉市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "市长与副市长", "overlap_org": "福泉市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "市长与副市长", "overlap_org": "福泉市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "市长与副市长", "overlap_org": "福泉市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "市长与副市长", "overlap_org": "福泉市人民政府", "overlap_period": "2026年"},
    # 人大 & 政协
    {"person_a": 1, "person_b": 16, "type": "overlap",
     "context": "市委书记与市人大常委会主任", "overlap_org": "福泉市", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 23, "type": "overlap",
     "context": "市委书记与市政协主席", "overlap_org": "福泉市", "overlap_period": "2026年"},
    # 市委常委同事关系
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "市委副书记与市委常委", "overlap_org": "中共福泉市委常委会", "overlap_period": "2026年"},
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "市委副书记与市委常委", "overlap_org": "中共福泉市委常委会", "overlap_period": "2026年"},
]


if __name__ == "__main__":
    db = DB_PATH
    gexf = GEXF_PATH

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db,
        gexf_path=gexf,
    )

    print(f"Build complete: {SLUG}")
    print(f"  DB:   {db}")
    print(f"  GEXF: {gexf}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
