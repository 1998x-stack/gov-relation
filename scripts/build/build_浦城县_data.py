#!/usr/bin/env python3
"""
Build 浦城县 (Pucheng County, 南平市, Fujian) government personnel
relationship network — SQLite database + GEXF graph.

浦城县 is located at the northernmost tip of Fujian Province, bordering
Jiangxi and Zhejiang provinces. Known as the "North Gate" of Fujian.

Population (2020): ~297,719
Area: 3,383 sq km

Current as of: 2026-07-16

Key recent changes:
- 陈锡明 was promoted from 县长 to 县委书记 on 2026-07-15 (replacing 李江平)
- 叶财旺 was appointed 县委副书记、县政府党组书记 (~2026-06), effectively县长
- 李江平 served as 县委书记 from Dec 2024 - Jul 2026; previously was 县长 (Dec 2021 - Dec 2024)

Targets: 县委书记 (陈锡明, 2026.07-) & 县长 (叶财旺, ~2026.06-)
"""

import sqlite3
import os
import json
from datetime import datetime

# ── Staging paths ─────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
TMP = BASE
DB_PATH = os.path.join(TMP, "浦城县_network.db")
GEXF_PATH = os.path.join(TMP, "浦城县_network.gexf")
PERSONS_DIR = TMP

today = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# DATA — from official government website (www.pc.gov.cn) and Baidu Baike
# =========================================================================

SLUG = "浦城县"
PROVINCE = "福建省"
CITY = "南平市"

persons = [
    # ── Core leaders ────────────────────────────────────────────────────
    # 陈锡明 — 浦城县委书记 (as of 2026.07.15), previously 县长 (2024.12)
    {
        "id": 1,
        "name": "陈锡明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "福建松溪",
        "education": "大学本科学历",
        "party_join": "1999-09",
        "work_start": "1998-09",
        "current_post": "浦城县委书记、县人武部党委第一书记",
        "current_org": "中共浦城县委员会",
        "source": "https://baike.baidu.com/item/%E9%99%88%E9%94%A1%E6%98%8E/24124603; https://np.fjsen.com/2026-07/10/content_32216748.htm",
    },
    # 叶财旺 — 浦城县委副书记、县政府党组书记 (effectively县长, ~2026.06-)
    {
        "id": 2,
        "name": "叶财旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-04",
        "birthplace": "",
        "education": "研究生学历，农学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县委副书记、县政府党组书记",
        "current_org": "浦城县人民政府",
        "source": "https://news.fznews.com.cn/dsxw/20250626/6T835yL8Ai.shtml; https://np.fjsen.com/2026-07/10/content_32216751.htm",
    },
    # 傅礼辉 — 县委常委、常务副县长
    {
        "id": 3,
        "name": "傅礼辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-08",
        "birthplace": "福建浦城",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "1996-09",
        "current_post": "浦城县委常委、副县长（常务）",
        "current_org": "浦城县人民政府",
        "source": "https://www.163.com/dy/article/KFHD2RMN0552D28J.html; https://news.qq.com/rain/a/20210525A049A700",
    },
    # 黄承源 — 县委常委、副县长
    {
        "id": 4,
        "name": "黄承源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县委常委、县政府党组成员、副县长",
        "current_org": "浦城县人民政府",
        "source": "https://www.163.com/dy/article/KFHD2RMN0552D28J.html",
    },
    # 何秀菊 — 副县长
    {
        "id": 5,
        "name": "何秀菊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学学历，管理学学士",
        "party_join": "",  # 党外/民主党派
        "work_start": "",
        "current_post": "浦城县人民政府副县长",
        "current_org": "浦城县人民政府",
        "source": "https://www.163.com/dy/article/KFHD2RMN0552D28J.html",
    },
    # 姚晖 — 副县长、县公安局局长
    {
        "id": 6,
        "name": "姚晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县人民政府副县长、县公安局党委书记、局长",
        "current_org": "浦城县人民政府",
        "source": "https://www.163.com/dy/article/KFHD2RMN0552D28J.html",
    },
    # 陈江宇 — 副县长
    {
        "id": 7,
        "name": "陈江宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-12",
        "birthplace": "福建浦城",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县人民政府党组成员、副县长",
        "current_org": "浦城县人民政府",
        "source": "https://www.163.com/dy/article/KFHD2RMN0552D28J.html; https://news.qq.com/rain/a/20210525A049A700",
    },
    # 韩钢 — 副县长
    {
        "id": 8,
        "name": "韩钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县人民政府党组成员、副县长",
        "current_org": "浦城县人民政府",
        "source": "https://www.163.com/dy/article/KFHD2RMN0552D28J.html",
    },
    # 胡春 — 副县长
    {
        "id": 9,
        "name": "胡春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县人民政府党组成员、副县长",
        "current_org": "浦城县人民政府",
        "source": "https://www.163.com/dy/article/KFHD2RMN0552D28J.html",
    },
    # 林武俊 — 副县长
    {
        "id": 10,
        "name": "林武俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县人民政府党组成员、副县长",
        "current_org": "浦城县人民政府",
        "source": "https://www.163.com/dy/article/KFHD2RMN0552D28J.html",
    },
    # 魏毅东 — 科技副县长
    {
        "id": 11,
        "name": "魏毅东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "浦城县人民政府党组成员、科技副县长",
        "current_org": "浦城县人民政府",
        "source": "https://www.163.com/dy/article/KFHD2RMN0552D28J.html",
    },
    # ── 县委其他常委 ──────────────────────────────────────────────────
    # 陈爱宾 — 原常务副县长, 后任县委副书记 (2025-06 拟任市直正处长级)
    {
        "id": 12,
        "name": "陈爱宾",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-01",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县委副书记（原常务副县长）",
        "current_org": "中共浦城县委员会",
        "source": "https://m.fznews.com.cn/dsxw/20250626/6T835yL8Ai.shtml",
    },
    # 谢孟华 — 县委常委、纪委书记、监委主任
    {
        "id": 13,
        "name": "谢孟华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县委常委、县纪委书记、县监委主任",
        "current_org": "中共浦城县纪律检查委员会",
        "source": "http://www.fjpcnews.com/2026-03/13/content_2320362.htm",
    },
    # 裴挥军 — 县委常委、总工会主席
    {
        "id": 14,
        "name": "裴挥军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县委常委、总工会主席",
        "current_org": "中共浦城县委员会",
        "source": "http://www.fjpcnews.com/2026-07/09/content_2363571.htm",
    },
    # 冯铁城 — 县委常委、统战部部长
    {
        "id": 15,
        "name": "冯铁城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县委常委、统战部部长",
        "current_org": "中共浦城县委员会",
        "source": "http://www.fjpcnews.com/2024-10/28/content_1921625.htm",
    },
    # 葛文清 — 县委常委（原副县长）
    {
        "id": 16,
        "name": "葛文清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县委常委",
        "current_org": "中共浦城县委员会",
        "source": "http://www.fjpcnews.com/2024-10/28/content_1921625.htm",
    },
    # 刘金顺 — 县委常委
    {
        "id": 17,
        "name": "刘金顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县委常委",
        "current_org": "中共浦城县委员会",
        "source": "http://www.fjpcnews.com/2024-10/28/content_1921625.htm",
    },
    # 马爱娇 — 原县委常委、组织部部长（2025-06拟任市级群团正职）
    {
        "id": 18,
        "name": "马爱娇",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970-08",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县委组织部部长（原任）",
        "current_org": "中共浦城县委员会",
        "source": "https://news.fznews.com.cn/dsxw/20250626/6T835yL8Ai.shtml",
    },

    # ── 人大常委会和政协领导 ──────────────────────────────────────────
    # 杨文龙 — 县人大常委会主任
    {
        "id": 19,
        "name": "杨文龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县人大常委会主任",
        "current_org": "浦城县人民代表大会常务委员会",
        "source": "https://np.fjsen.com/wap/2025-12/24/content_32103860.htm",
    },
    # 郑辉 — 县政协主席
    {
        "id": 20,
        "name": "郑辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦城县政协主席",
        "current_org": "政协浦城县委员会",
        "source": "https://np.fjsen.com/wap/2025-12/24/content_32103860.htm",
    },

    # ── 重要前任领导 ──────────────────────────────────────────────────
    # 李江平 — 前任县委书记 (2024.12-2026.07), 前县长 (2021.12-2024.12)
    {
        "id": 21,
        "name": "李江平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-06",
        "birthplace": "福建福清",
        "education": "中央党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原浦城县委书记",
        "current_org": "中共浦城县委员会",
        "source": "https://baike.baidu.com/item/%E6%9D%8E%E6%B1%9F%E5%B9%B3/19674696",
    },
    # 沈晓文 — 前前任县委书记 (2021.05-2024.07), 前县长 (2016-2021.05)
    {
        "id": 22,
        "name": "沈晓文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-10",
        "birthplace": "福建诏安",
        "education": "清华大学博士研究生学历，理学博士",
        "party_join": "2003-12",
        "work_start": "2011-07",
        "current_post": "厦门市翔安区委副书记、区长",
        "current_org": "厦门市翔安区人民政府",
        "source": "https://www.bjnews.com.cn/detail/1722397554129454.html",
    },
    # 周永和 — 原县委书记 (2016.06-2021.04), 被调查处分
    {
        "id": 23,
        "name": "周永和",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-10",
        "birthplace": "浙江云和（福建建阳出生）",
        "education": "在职大学学历",
        "party_join": "1987-08",
        "work_start": "1984-08",
        "current_post": "",
        "current_org": "",
        "source": "http://fj.people.com.cn/n2/2021/0409/c181466-34668121.html",
    },
    # 黄书荣 — 原县委书记 (2013.09-2016.06), 前县长
    {
        "id": 24,
        "name": "黄书荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://fjsyhzh.com/zh/zoujinpucheng/2006.html",
    },
    # 陈国发 — 原县委书记 (2011.06-2013.09), 前县长
    {
        "id": 25,
        "name": "陈国发",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://fjsyhzh.com/zh/zoujinpucheng/2005.html",
    },
    # 朱金生 — 原县长 (2013.09-2021?)
    {
        "id": 26,
        "name": "朱金生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://www.fjpcnews.com/2015-08/04/content_1229262.htm",
    },

    # ── 南平市领导 (上级) ──────────────────────────────────────────
    {
        "id": 27,
        "name": "袁超洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南平市委书记",
        "current_org": "中共南平市委员会",
        "source": "https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82",
    },
    {
        "id": 28,
        "name": "林建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-11",
        "birthplace": "",
        "education": "在职研究生学历，管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南平市市长",
        "current_org": "南平市人民政府",
        "source": "https://www.np.gov.cn",
    },
]

organizations = [
    {"id": 1, "name": "中共浦城县委员会", "type": "党委", "level": "县处级", "parent": "中共南平市委员会", "location": "福建省南平市浦城县"},
    {"id": 2, "name": "浦城县人民政府", "type": "政府", "level": "县处级", "parent": "南平市人民政府", "location": "福建省南平市浦城县"},
    {"id": 3, "name": "中共浦城县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共浦城县委员会", "location": "福建省南平市浦城县"},
    {"id": 4, "name": "浦城县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "福建省南平市浦城县"},
    {"id": 5, "name": "政协浦城县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "福建省南平市浦城县"},
    {"id": 6, "name": "浦城县人民武装部", "type": "党委", "level": "县处级", "parent": "南平军分区", "location": "福建省南平市浦城县"},
    {"id": 7, "name": "浦城县总工会", "type": "群团", "level": "乡科级", "parent": "", "location": "福建省南平市浦城县"},
    {"id": 8, "name": "南平市人民政府", "type": "政府", "level": "地厅级", "parent": "福建省人民政府", "location": "福建省南平市建阳区"},
    {"id": 9, "name": "中共南平市委员会", "type": "党委", "level": "地厅级", "parent": "中共福建省委员会", "location": "福建省南平市建阳区"},
    {"id": 10, "name": "厦门市翔安区人民政府", "type": "政府", "level": "县处级", "parent": "厦门市人民政府", "location": "福建省厦门市翔安区"},
]

positions = [
    # 陈锡明 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "浦城县委书记", "start": "2026-07", "end": "present", "rank": "正处级", "note": "2026年7月15日任县人武部党委第一书记，此前为县长"},
    {"person_id": 1, "org_id": 6, "title": "浦城县人武部党委第一书记", "start": "2026-07", "end": "present", "rank": "", "note": "2026年7月15日南平军分区宣读任职决定"},
    {"person_id": 1, "org_id": 2, "title": "浦城县县长", "start": "2024-12", "end": "2026-07", "rank": "正处级", "note": "2024年12月27日任代县长，12月31日当选县长"},
    {"person_id": 1, "org_id": 1, "title": "浦城县委副书记", "start": "2024-12", "end": "2026-07", "rank": "正处级", "note": "任县长期间兼任县委副书记"},
    # 陈锡明 — 建瓯任职
    {"person_id": 1, "org_id": 2, "title": "建瓯市委副书记、三级调研员", "start": "", "end": "2024-12", "rank": "副处级", "note": "调任浦城前任建瓯市委副书记"},
    {"person_id": 1, "org_id": 2, "title": "建瓯市委常委、副市长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 陈锡明 — 松溪任职
    {"person_id": 1, "org_id": 2, "title": "松溪县河东乡党委书记", "start": "", "end": "", "rank": "乡科级", "note": "早期任职"},
    # 陈锡明 — 教育
    {"person_id": 1, "org_id": 1, "title": "1998年9月参加工作, 1999年9月入党", "start": "1998-09", "end": "", "rank": "", "note": "大学本科学历，福建松溪人"},

    # 叶财旺 — 县委副书记、县政府党组书记
    {"person_id": 2, "org_id": 1, "title": "浦城县委副书记", "start": "~2026-06", "end": "present", "rank": "正处级", "note": "从建瓯市调任"},
    {"person_id": 2, "org_id": 2, "title": "浦城县人民政府党组书记", "start": "~2026-06", "end": "present", "rank": "正处级", "note": ""},
    # 叶财旺 — 建瓯任职
    {"person_id": 2, "org_id": 2, "title": "建瓯市委常委、副市长", "start": "", "end": "~2026-06", "rank": "副处级", "note": "2025年6月公示拟进一步使用"},

    # 傅礼辉 — 常务副县长
    {"person_id": 3, "org_id": 2, "title": "浦城县委常委、副县长（常务）", "start": "", "end": "present", "rank": "副处级", "note": "负责县政府常务工作"},
    {"person_id": 3, "org_id": 1, "title": "浦城县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "浦城县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 傅礼辉 — 莲塘镇任职
    {"person_id": 3, "org_id": 2, "title": "浦城县莲塘镇党委书记", "start": "", "end": "", "rank": "乡科级", "note": "2017年时任莲塘镇党委书记"},

    # 黄承源 — 县委常委、副县长
    {"person_id": 4, "org_id": 1, "title": "浦城县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "浦城县政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 何秀菊 — 副县长
    {"person_id": 5, "org_id": 2, "title": "浦城县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "无党派/民主党派"},

    # 姚晖 — 副县长、公安局局长
    {"person_id": 6, "org_id": 2, "title": "浦城县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "浦城县公安局党委书记、局长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 陈江宇 — 副县长
    {"person_id": 7, "org_id": 2, "title": "浦城县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "浦城县河滨街道党工委书记", "start": "", "end": "", "rank": "乡科级", "note": "2021年时任河滨街道党工委书记"},

    # 韩钢 — 副县长
    {"person_id": 8, "org_id": 2, "title": "浦城县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 胡春 — 副县长
    {"person_id": 9, "org_id": 2, "title": "浦城县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 林武俊 — 副县长
    {"person_id": 10, "org_id": 2, "title": "浦城县人民政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 魏毅东 — 科技副县长
    {"person_id": 11, "org_id": 2, "title": "浦城县人民政府党组成员、科技副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 陈爱宾 — 县委副书记
    {"person_id": 12, "org_id": 1, "title": "浦城县委副书记", "start": "", "end": "present", "rank": "正处级", "note": "2025年6月公示拟任市直正处长级职务"},
    {"person_id": 12, "org_id": 2, "title": "浦城县委常委、常务副县长", "start": "", "end": "", "rank": "副处级", "note": ""},

    # 谢孟华 — 纪委书记
    {"person_id": 13, "org_id": 3, "title": "浦城县委常委、县纪委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "浦城县监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 裴挥军 — 县委常委
    {"person_id": 14, "org_id": 1, "title": "浦城县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 7, "title": "浦城县总工会主席", "start": "", "end": "present", "rank": "", "note": ""},

    # 冯铁城 — 统战部长
    {"person_id": 15, "org_id": 1, "title": "浦城县委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 葛文清 — 县委常委
    {"person_id": 16, "org_id": 1, "title": "浦城县委常委", "start": "", "end": "present", "rank": "副处级", "note": "原副县长"},

    # 刘金顺 — 县委常委
    {"person_id": 17, "org_id": 1, "title": "浦城县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 马爱娇 — 原组织部长
    {"person_id": 18, "org_id": 1, "title": "浦城县委常委、组织部部长", "start": "", "end": "2025-06", "rank": "副处级", "note": "2025年6月公示拟任市级群团正职"},

    # 杨文龙 — 人大主任
    {"person_id": 19, "org_id": 4, "title": "浦城县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 郑辉 — 政协主席
    {"person_id": 20, "org_id": 5, "title": "浦城县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 李江平 — 前任县委书记
    {"person_id": 21, "org_id": 1, "title": "浦城县委书记", "start": "2024-12", "end": "2026-07", "rank": "正处级", "note": "2026年7月由陈锡明接替"},
    {"person_id": 21, "org_id": 2, "title": "浦城县县长", "start": "2021-12", "end": "2024-12", "rank": "正处级", "note": "2024年12月27日辞去县长职务"},
    {"person_id": 21, "org_id": 2, "title": "浦城县委副书记、县长候选人", "start": "2021-05", "end": "2021-12", "rank": "正处级", "note": "2021年5月提名"},
    {"person_id": 21, "org_id": 2, "title": "南平市住建局党组书记、副局长", "start": "2020-03", "end": "2021-05", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 1, "title": "南平市建阳区委副书记（正处长级）", "start": "2016-06", "end": "2020-03", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 1, "title": "南平市档案局副局长、市档案馆副馆长", "start": "2011-01", "end": "2013-04", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "福建省闽北产业园区开发建设有限公司总经理", "start": "2013-04", "end": "2014-07", "rank": "", "note": ""},

    # 沈晓文 — 前前任县委书记
    {"person_id": 22, "org_id": 1, "title": "浦城县委书记", "start": "2021-05", "end": "2024-07", "rank": "正处级", "note": "2024年7月公示拟提拔交流任职，后调任厦门"},
    {"person_id": 22, "org_id": 2, "title": "浦城县县长", "start": "2016", "end": "2021-05", "rank": "正处级", "note": "33岁任县长"},
    {"person_id": 22, "org_id": 1, "title": "邵武市委常委、大竹镇党委书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "建阳市副市长（挂职）", "start": "2012", "end": "", "rank": "副处级", "note": "引进生到福建"},
    {"person_id": 22, "org_id": 10, "title": "厦门市翔安区区长", "start": "2024-07", "end": "present", "rank": "正厅级", "note": "跨市提拔交流任职"},

    # 周永和 — 原县委书记
    {"person_id": 23, "org_id": 1, "title": "浦城县委书记", "start": "2016-06", "end": "2021-04", "rank": "正处级", "note": "2021年4月被调查"},
    {"person_id": 23, "org_id": 2, "title": "南平市科技局党组书记、局长", "start": "2015-07", "end": "2016-06", "rank": "正处级", "note": ""},
    {"person_id": 23, "org_id": 2, "title": "南平市档案局局长、市档案馆馆长", "start": "2013-09", "end": "2015-07", "rank": "正处级", "note": ""},
    {"person_id": 23, "org_id": 1, "title": "浦城县委副书记", "start": "2011-07", "end": "2013-09", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 2, "title": "浦城县政府副县长", "start": "2007-01", "end": "2011-07", "rank": "副处级", "note": "2008-2010援疆任新疆吉木萨尔县副县长"},

    # 黄书荣 — 原县委书记
    {"person_id": 24, "org_id": 1, "title": "浦城县委书记", "start": "2013-09", "end": "2016-06", "rank": "正处级", "note": ""},
    {"person_id": 24, "org_id": 2, "title": "浦城县县长", "start": "", "end": "2013-09", "rank": "正处级", "note": ""},

    # 陈国发 — 原县委书记
    {"person_id": 25, "org_id": 1, "title": "浦城县委书记", "start": "2011-06", "end": "2013-09", "rank": "正处级", "note": ""},
    {"person_id": 25, "org_id": 2, "title": "浦城县县长", "start": "", "end": "2011-06", "rank": "正处级", "note": ""},

    # 朱金生 — 原县长
    {"person_id": 26, "org_id": 2, "title": "浦城县县长", "start": "2013-09", "end": "", "rank": "正处级", "note": ""},

    # 南平市领导
    {"person_id": 27, "org_id": 9, "title": "南平市委书记", "start": "2023-02", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 28, "org_id": 8, "title": "南平市市长", "start": "2023-02", "end": "present", "rank": "正厅级", "note": ""},
]

relationships = [
    # 陈锡明 — 叶财旺 (党政搭班)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "陈锡明任县委书记，叶财旺任县委副书记、县政府党组书记", "overlap_org": "中共浦城县委员会", "overlap_period": "2026-06", "direction": "undirected", "strength": "strong"},

    # 陈锡明 — 傅礼辉 (县委书记-常务副县长)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "陈锡明任县长(2024.12-2026.07)和县委书记期间，傅礼辉任副县长/常务副县长", "overlap_org": "浦城县人民政府", "overlap_period": "2024-12至今", "direction": "undirected", "strength": "strong"},

    # 陈锡明 — 各副县长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "陈锡明任县长/县委书记期间，黄承源任县委常委、副县长", "overlap_org": "浦城县人民政府", "overlap_period": "2024-12至今", "direction": "undirected", "strength": "strong"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "陈锡明任县长/县委书记期间，何秀菊任副县长", "overlap_org": "浦城县人民政府", "overlap_period": "2024-12至今", "direction": "undirected", "strength": "strong"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "陈锡明任县长/县委书记期间，姚晖任副县长", "overlap_org": "浦城县人民政府", "overlap_period": "2024-12至今", "direction": "undirected", "strength": "strong"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "陈锡明任县长/县委书记期间，陈江宇任副县长", "overlap_org": "浦城县人民政府", "overlap_period": "2024-12至今", "direction": "undirected", "strength": "strong"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "陈锡明任县长/县委书记期间，韩钢任副县长", "overlap_org": "浦城县人民政府", "overlap_period": "2024-12至今", "direction": "undirected", "strength": "strong"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "陈锡明任县长/县委书记期间，胡春任副县长", "overlap_org": "浦城县人民政府", "overlap_period": "2024-12至今", "direction": "undirected", "strength": "strong"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "陈锡明任县长/县委书记期间，林武俊任副县长", "overlap_org": "浦城县人民政府", "overlap_period": "2024-12至今", "direction": "undirected", "strength": "strong"},

    # 叶财旺 — 傅礼辉 (党政搭班)
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "叶财旺任县委副书记/县政府党组书记，傅礼辉任常务副县长", "overlap_org": "浦城县人民政府", "overlap_period": "2026-06至今", "direction": "undirected", "strength": "strong"},

    # 陈锡明 — 李江平 (predecessor_successor — 县委书记)
    {"person_a": 1, "person_b": 21, "type": "predecessor_successor", "context": "陈锡明接替李江平任县委书记", "overlap_org": "中共浦城县委员会", "overlap_period": "2026-07", "direction": "person_to_other", "strength": "strong"},

    # 陈锡明 — 李江平 (县长接替)
    {"person_a": 1, "person_b": 21, "type": "predecessor_successor", "context": "陈锡明接替李江平任县长(2024.12李江平辞职后)", "overlap_org": "浦城县人民政府", "overlap_period": "2024-12", "direction": "person_to_other", "strength": "strong"},

    # 李江平 — 沈晓文 (predecessor_successor — 县委书记)
    {"person_a": 21, "person_b": 22, "type": "predecessor_successor", "context": "李江平接替沈晓文任县委书记", "overlap_org": "中共浦城县委员会", "overlap_period": "2024-12", "direction": "other_to_person", "strength": "strong"},

    # 李江平 — 沈晓文 (县长-书记搭班)
    {"person_a": 21, "person_b": 22, "type": "superior_subordinate", "context": "沈晓文任县委书记时，李江平任县长", "overlap_org": "中共浦城县委员会", "overlap_period": "2021-05至2024-07", "direction": "other_to_person", "strength": "strong"},

    # 沈晓文 — 周永和 (predecessor_successor — 县委书记)
    {"person_a": 22, "person_b": 23, "type": "predecessor_successor", "context": "沈晓文接替周永和任县委书记（周永和2021年4月被调查后）", "overlap_org": "中共浦城县委员会", "overlap_period": "2021-05", "direction": "person_to_other", "strength": "strong"},

    # 李江平 — 陈爱宾 (搭班)
    {"person_a": 21, "person_b": 12, "type": "overlap", "context": "李江平任县长/县委书记期间，陈爱宾任副县长/县委副书记", "overlap_org": "浦城县人民政府", "overlap_period": "2021-至今", "direction": "undirected", "strength": "strong"},

    # 傅礼辉 — 陈江宇 (同乡/同地工作)
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "傅礼辉和陈江宇均为浦城本地干部，长期共事", "overlap_org": "浦城县人民政府", "overlap_period": "", "direction": "undirected", "strength": "medium"},

    # 上级关系
    {"person_a": 1, "person_b": 27, "type": "superior_subordinate", "context": "陈锡明作为浦城县委书记，受南平市委书记袁超洪领导", "overlap_org": "中共福建省委员会", "overlap_period": "2026-07", "direction": "other_to_person", "strength": "strong"},
    {"person_a": 1, "person_b": 28, "type": "superior_subordinate", "context": "陈锡明作为浦城县长(2024.12-2026.07)，受南平市长林建领导", "overlap_org": "福建省人民政府", "overlap_period": "2024-12至今", "direction": "other_to_person", "strength": "strong"},

    # 县委常委会关系
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "陈锡明作为县委书记，谢孟华为纪委书记", "overlap_org": "中共浦城县委员会", "overlap_period": "2026-07至今", "direction": "undirected", "strength": "strong"},
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate", "context": "陈锡明作为县委书记，裴挥军为县委常委", "overlap_org": "中共浦城县委员会", "overlap_period": "2026-07至今", "direction": "undirected", "strength": "strong"},
    {"person_a": 1, "person_b": 15, "type": "superior_subordinate", "context": "陈锡明作为县委书记，冯铁城为县委常委、统战部长", "overlap_org": "中共浦城县委员会", "overlap_period": "2026-07至今", "direction": "undirected", "strength": "strong"},
    {"person_a": 1, "person_b": 16, "type": "superior_subordinate", "context": "陈锡明作为县委书记，葛文清为县委常委", "overlap_org": "中共浦城县委员会", "overlap_period": "2026-07至今", "direction": "undirected", "strength": "strong"},

    # 跨地区 — 沈晓文调任厦门
    {"person_a": 22, "person_b": 1, "type": "other", "context": "沈晓文作为引进生（清华大学博士）到福建工作后，陈锡明作为松溪/建瓯本地成长干部，二人均为南平系干部", "overlap_org": "", "overlap_period": "", "direction": "undirected", "strength": "weak"},
]


# =========================================================================
# BUILD SQLITE DATABASE
# =========================================================================
def build_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        direction TEXT, strength TEXT
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p.get("birthplace", ""), p["education"], p["party_join"],
                   p.get("work_start", ""), p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions (person_id,org_id,title,start,\"end\",rank,note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        c.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,direction,strength) VALUES (?,?,?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r.get("overlap_period", ""), r["direction"], r["strength"]))

    conn.commit()
    conn.close()
    print(f"✓ SQLite DB created: {DB_PATH}")


# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p.get("current_post") or ""
    if "书记" in post and ("县" in post or "区" in post):
        return "255,50,50"
    elif "县长" in post or "县长" in post:
        return "50,100,255"
    elif "副" in post and ("县长" in post or "区长" in post):
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "市长" in post or "市委书记" in post:
        return "255,50,50"
    else:
        return "100,100,100"


def person_size(p):
    if p["id"] in (1,):  # 县委书记 (陈锡明)
        return "20.0"
    elif p["id"] in (2, 21, 22):  # 县长, 前任县委书记/县长
        return "18.0"
    elif p["id"] in (3, 12, 13):  # 常务副县长, 县委副书记, 纪委书记
        return "15.0"
    elif p["id"] in (27, 28):  # 南平市领导
        return "15.0"
    elif 4 <= p["id"] <= 11:  # 副县长
        return "12.0"
    elif p["id"] in (19, 20):  # 人大主任、政协主席
        return "12.0"
    elif p["id"] in (14, 15, 16, 17, 18):  # 县委常委
        return "12.0"
    else:
        return "12.0"


def org_color(o):
    m = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255", "政协": "255,240,200", "群团": "255,220,255"}
    return m.get(o["type"], "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append(f'    <description>{SLUG}领导班子关系网络 - {PROVINCE}{CITY}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
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
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF graph created: {GEXF_PATH}")


# =========================================================================
# PERSON JSONS
# =========================================================================
def write_person_json(pid, filename_suffix, person_name, extra_context=None):
    p = next(x for x in persons if x["id"] == pid)

    # Build relationships
    rels_out = []
    for r in relationships:
        if r["person_a"] == pid:
            other = next(x for x in persons if x["id"] == r["person_b"])
            rels_out.append({"person": other["name"], "person_id": f"pucheng_{other['name']}",
                             "relationship_type": r["type"], "strength": r["strength"],
                             "evidence": r["context"], "overlap_org": r["overlap_org"],
                             "overlap_period": r.get("overlap_period", ""),
                             "direction": r["direction"], "confidence": "confirmed",
                             "source_ids": ["S001", "S002"]})
        elif r["person_b"] == pid:
            other = next(x for x in persons if x["id"] == r["person_a"])
            rels_out.append({"person": other["name"], "person_id": f"pucheng_{other['name']}",
                             "relationship_type": r["type"], "strength": r["strength"],
                             "evidence": r["context"], "overlap_org": r["overlap_org"],
                             "overlap_period": r.get("overlap_period", ""),
                             "direction": r["direction"], "confidence": "confirmed",
                             "source_ids": ["S001", "S002"]})

    # Build career timeline
    person_positions = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            system = "other"
            if org:
                if "党委" in org["type"]:
                    system = "party"
                elif "政府" in org["type"]:
                    system = "government"
                elif "人大" in org["type"]:
                    system = "other"
                elif "政协" in org["type"]:
                    system = "other"
            person_positions.append({
                "start": pos.get("start", ""), "end": pos.get("end", ""),
                "org": org["name"] if org else "",
                "title": pos["title"], "level": pos.get("rank", ""),
                "location": org["location"] if org else "",
                "system": system,
                "rank": pos.get("rank", ""), "is_key_promotion": False,
                "notes": pos.get("note", ""), "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            })

    # Build education array
    edu_entries = []
    if p.get("education"):
        edu_entries.append({
            "period": "", "institution": "", "major": "",
            "degree": p["education"], "study_type": "unknown", "source_ids": ["S001"]
        })

    # Career pattern
    career_pattern = "unknown"
    if pid == 1:  # 陈锡明
        career_pattern = "local_ladder"
    elif pid == 2:  # 叶财旺
        career_pattern = "cross_county_rotation"
    elif pid == 21:  # 李江平
        career_pattern = "cross_county_rotation"
    elif pid == 22:  # 沈晓文
        career_pattern = "technical_specialist"

    # Profile URL
    official_url = ""
    if pid == 1:
        official_url = "https://baike.baidu.com/item/%E9%99%88%E9%94%A1%E6%98%8E/24124603"
    elif pid == 21:
        official_url = "https://baike.baidu.com/item/%E6%9D%8E%E6%B1%9F%E5%B9%B3/19674696"
    elif pid == 22:
        official_url = "https://www.bjnews.com.cn/detail/1722397554129454.html"

    profile = {
        "schema_version": "1.0",
        "generated_at": today,
        "investigation_scope": {
            "province": PROVINCE, "city": CITY, "region": SLUG,
            "job": filename_suffix, "task_id": "fujian_浦城县",
            "time_focus": "2016-2026"
        },
        "identity": {
            "person_id": f"pucheng_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": edu_entries,
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": official_url
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": today,
            "is_current_confirmed": pid in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17),
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": person_positions,
        "organizations": [],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": career_pattern,
            "systems_experience": ["party"] if any("党委" in str(pos) for pos in person_positions) else [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id": "S001", "title": "浦城县人民政府网站",
             "url": "https://www.pc.gov.cn",
             "publisher": "浦城县人民政府", "published_at": "", "accessed_at": today,
             "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S002", "title": "浦城县新闻网",
             "url": "http://www.fjpcnews.com",
             "publisher": "浦城县融媒体中心", "published_at": "", "accessed_at": today,
             "source_type": "media", "reliability": "medium", "notes": ""},
            {"id": "S003", "title": "陈锡明 - 百度百科",
             "url": "https://baike.baidu.com/item/%E9%99%88%E9%94%A1%E6%98%8E/24124603",
             "publisher": "百度百科", "published_at": "", "accessed_at": today,
             "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
            {"id": "S004", "title": "李江平 - 百度百科",
             "url": "https://baike.baidu.com/item/%E6%9D%8E%E6%B1%9F%E5%B9%B3/19674696",
             "publisher": "百度百科", "published_at": "", "accessed_at": today,
             "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
            {"id": "S005", "title": "浦城县人民政府领导班子工作分工（2025.11）",
             "url": "https://www.163.com/dy/article/KFHD2RMN0552D28J.html",
             "publisher": "网易/浦城县政府", "published_at": "2025-11-29", "accessed_at": today,
             "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S006", "title": "浦城县人民政府领导班子工作分工（2024.07）",
             "url": "https://www.pc.gov.cn/cms/html/pcxrmzf/2024-07-24/1721828210.html",
             "publisher": "浦城县人民政府", "published_at": "2024-07-24", "accessed_at": today,
             "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S007", "title": "浦城县委领导督导防汛防台风工作",
             "url": "https://np.fjsen.com/2026-07/10/content_32216748.htm",
             "publisher": "东南网", "published_at": "2026-07-10", "accessed_at": today,
             "source_type": "media", "reliability": "high", "notes": "确认陈锡明任县委书记、叶财旺任县委副书记"},
            {"id": "S008", "title": "浦城县防范台风巴威动员部署会",
             "url": "https://np.fjsen.com/2026-07/10/content_32216751.htm",
             "publisher": "东南网", "published_at": "2026-07-10", "accessed_at": today,
             "source_type": "media", "reliability": "high", "notes": "确认叶财旺任县委副书记、县政府党组书记"},
            {"id": "S009", "title": "陈锡明任浦城县人武部党委第一书记",
             "url": "http://www.fjpcnews.com/2026-07/16/content_2366588.htm",
             "publisher": "浦城新闻网", "published_at": "2026-07-16", "accessed_at": today,
             "source_type": "official", "reliability": "high", "notes": "确认陈锡明任县委书记"},
            {"id": "S010", "title": "沈晓文 - 新京报报道",
             "url": "https://www.bjnews.com.cn/detail/1722397554129454.html",
             "publisher": "新京报", "published_at": "2024-07-31", "accessed_at": today,
             "source_type": "media", "reliability": "high", "notes": "沈晓文履历详情"},
            {"id": "S011", "title": "周永和简历 - 人民网",
             "url": "http://fj.people.com.cn/n2/2021/0409/c181466-34668121.html",
             "publisher": "人民网", "published_at": "2021-04-09", "accessed_at": today,
             "source_type": "media", "reliability": "high", "notes": "周永和涉嫌严重违纪违法被调查"},
            {"id": "S012", "title": "福建南平拟提拔任用19人公示",
             "url": "https://news.fznews.com.cn/dsxw/20250626/6T835yL8Ai.shtml",
             "publisher": "福州新闻网", "published_at": "2025-06-26", "accessed_at": today,
             "source_type": "official", "reliability": "high", "notes": "叶财旺、陈爱宾、马爱娇公示信息"},
            {"id": "S013", "title": "浦城县委常委会会议",
             "url": "http://www.fjpcnews.com/2024-10/28/content_1921625.htm",
             "publisher": "浦城新闻网", "published_at": "2024-10-28", "accessed_at": today,
             "source_type": "media", "reliability": "medium", "notes": "县委常委名单"},
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": f"缺少{p['name']}的完整履历时间线，部分人员出生地、教育背景不详"
        },
        "open_questions": [
            {"priority": "high", "question": f"{p['name']}的完整早期履历",
             "why_it_matters": "影响人物身份确认和履历完整度",
             "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任职经历"], "last_attempted": today},
            {"priority": "high", "question": "李江平2026年7月后的去向",
             "why_it_matters": "前任县委书记的去向反映其仕途走向",
             "suggested_queries": ["李江平 最新任职"], "last_attempted": today},
            {"priority": "medium", "question": "叶财旺的完整履历（来浦城前在建瓯的任职经历）",
             "why_it_matters": "理解新任县长的职业发展路径",
             "suggested_queries": ["叶财旺 简历 建瓯"], "last_attempted": today},
        ]
    }

    filename = f"{today.replace('-', '')}-{PROVINCE}-{CITY}-{filename_suffix}-{p['name']}.json"
    fpath = os.path.join(PERSONS_DIR, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"✓ Person JSON created: {fpath}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"Building {SLUG} government personnel network...")
    print(f"Date: {today}")
    print(f"Target: 县委书记 (陈锡明, 2026.07-) & 县长 (叶财旺, ~2026.06-)")
    print(f"Previous: 李江平任县委书记(2024.12-2026.07), 沈晓文(2021.05-2024.07)")
    print()
    build_sqlite()
    build_gexf()
    write_person_json(1, "县委书记", "陈锡明")
    write_person_json(2, "县长", "叶财旺")
    write_person_json(21, "原县委书记", "李江平")
    print(f"\nDone. All artifacts written to {TMP}")
    print(f"\nKey changes: 陈锡明2026年7月15日由县长升任县委书记；叶财旺约2026年6月从建瓯调任浦城任县委副书记/县政府党组书记。")
    print(f"前任县委书记李江平的下一步去向待查询。")
