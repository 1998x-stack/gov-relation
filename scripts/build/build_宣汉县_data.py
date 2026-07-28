#!/usr/bin/env python3
"""宣汉县（达州市）领导班子关系网络数据生成脚本。

Targets: 县委书记 杨勇, 县长 陈军
Data as of: 2026-07-28
Sources: 宣汉县人民政府官网 (www.xuanhan.gov.cn), 百度百科
"""

import json
import os
import sqlite3
from datetime import datetime

TASK_ID = "sichuan_宣汉县"
SLUG = "宣汉县"
AS_OF = "2026-07-28"
PROVINCE = "四川省"
PARENT_CITY = "达州市"

BASE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "data/tmp/sichuan_宣汉县"
_BASE_OVERRIDE = os.environ.get("XUANHAN_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "宣汉县_network.db")
GEXF_PATH = os.path.join(BASE, "宣汉县_network.gexf")
PERSONS_DIR = os.path.join(BASE, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

persons = [
    # 1 - 县委书记
    {
        "id": 1,
        "name": "杨勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年2月",
        "birthplace": "达州市达川区",
        "education": "四川省委党校函授学院法律专业（在职大学）",
        "party_join": "1996年12月",
        "work_start": "1991年9月",
        "current_post": "达州市人民政府党组成员、副市长，宣汉县委书记",
        "current_org": "中共宣汉县委员会",
        "source": "http://www.xuanhan.gov.cn/news-list-nixinjianli.html",
    },
    # 2 — 县长
    {
        "id": 2,
        "name": "陈军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年12月",
        "birthplace": "四川开江",
        "education": "大学",
        "party_join": "",
        "work_start": "1996年8月",
        "current_post": "中共宣汉县委副书记，宣汉县人民政府党组书记、县长",
        "current_org": "宣汉县人民政府",
        "source": "http://www.xuanhan.gov.cn/news-list-ztjl.html",
    },
    # 3 — 县委副书记（专职）
    {
        "id": 3,
        "name": "杨轶",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共宣汉县委副书记",
        "current_org": "中共宣汉县委员会",
        "source": "https://baike.baidu.com/item/中国共产党宣汉县委员会",
    },
    # 4 — 县委副书记（专职）
    {
        "id": 4,
        "name": "吴中凡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共宣汉县委副书记",
        "current_org": "中共宣汉县委员会",
        "source": "https://baike.baidu.com/item/中国共产党宣汉县委员会",
    },
    # 5 — 县委常委、常务副县长
    {
        "id": 5,
        "name": "李静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年1月",
        "birthplace": "四川万源",
        "education": "大学，经济学学士",
        "party_join": "2007年11月",
        "work_start": "2009年7月",
        "current_post": "中共宣汉县委常委，宣汉县人民政府党组副书记、常务副县长",
        "current_org": "宣汉县人民政府",
        "source": "http://www.xuanhan.gov.cn/news-list-lijing.html",
    },
    # 6 — 县委常委、副县长（挂职）
    {
        "id": 6,
        "name": "叶仙富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "达州市人民政府副秘书长、中共宣汉县委常委、宣汉县人民政府党组成员、副县长（挂职三年）",
        "current_org": "宣汉县人民政府",
        "source": "http://www.xuanhan.gov.cn/news-list-ldzc.html",
    },
    # 7 — 县委常委、副县长
    {
        "id": 7,
        "name": "潘攀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共宣汉县委常委、宣汉县人民政府党组成员、副县长",
        "current_org": "宣汉县人民政府",
        "source": "http://www.xuanhan.gov.cn/news-list-ldzc.html",
    },
    # 8 — 县委常委、副县长
    {
        "id": 8,
        "name": "李京晏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "1994年9月",
        "current_post": "中共宣汉县委常委、宣汉县人民政府党组成员、副县长",
        "current_org": "宣汉县人民政府",
        "source": "http://www.xuanhan.gov.cn/news-list-lijingyan.html",
    },
    # 9 — 副县长、公安局长
    {
        "id": 9,
        "name": "陈刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "四川大学自考法律专业本科",
        "party_join": "",
        "work_start": "1997年8月",
        "current_post": "宣汉县人民政府党组成员、副县长，县委政法委副书记（兼），县公安局党委书记、局长、督察长（兼）",
        "current_org": "宣汉县公安局",
        "source": "http://www.xuanhan.gov.cn/news-list-chengang.html",
    },
    # 10 — 副县长
    {
        "id": 10,
        "name": "胡锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "英国帝国理工学院博士（能源政策）",
        "party_join": "",
        "work_start": "2013年9月",
        "current_post": "宣汉县人民政府党组成员、副县长",
        "current_org": "宣汉县人民政府",
        "source": "http://www.xuanhan.gov.cn/news-list-hurui.html",
    },
    # 11 — 副县长
    {
        "id": 11,
        "name": "林兰忻",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "中科院过程工程研究所工学博士（化学工艺）",
        "party_join": "",
        "work_start": "2017年7月",
        "current_post": "宣汉县人民政府副县长",
        "current_org": "宣汉县人民政府",
        "source": "http://www.xuanhan.gov.cn/news-list-linlanxin.html",
    },
    # 12 — 副县长（2026年新任）
    {
        "id": 12,
        "name": "周颜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "河南理工大学电子信息科学与技术专业",
        "party_join": "",
        "work_start": "2009年9月",
        "current_post": "宣汉县人民政府党组成员、副县长",
        "current_org": "宣汉县人民政府",
        "source": "http://www.xuanhan.gov.cn/news-list-zhouyan.html",
    },
    # 13 — 前任县委书记（冯永刚）
    {
        "id": 13,
        "name": "冯永刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年1月",
        "birthplace": "通川区",
        "education": "党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/item/冯永刚/63127651",
    },
    # 14 — 前任县委书记（唐廷教，冯永刚的前任）
    {
        "id": 14,
        "name": "唐廷教",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/item/唐廷教",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共宣汉县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共达州市委员会",
        "location": "宣汉县",
    },
    {
        "id": 2,
        "name": "宣汉县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "达州市人民政府",
        "location": "宣汉县",
    },
    {
        "id": 3,
        "name": "宣汉县公安局",
        "type": "政府",
        "level": "县",
        "parent": "宣汉县人民政府",
        "location": "宣汉县",
    },
    {
        "id": 4,
        "name": "达州市人民政府",
        "type": "政府",
        "level": "市",
        "parent": "四川省人民政府",
        "location": "达州市",
    },
    {
        "id": 5,
        "name": "中国共产党达州市委员会",
        "type": "党委",
        "level": "市",
        "parent": "中共四川省委员会",
        "location": "达州市",
    },
    {
        "id": 6,
        "name": "达州经济开发区",
        "type": "开发区",
        "level": "县",
        "parent": "达州市人民政府",
        "location": "达州市",
    },
    {
        "id": 7,
        "name": "达州市农业农村局",
        "type": "政府",
        "level": "市",
        "parent": "达州市人民政府",
        "location": "达州市",
    },
    {
        "id": 8,
        "name": "达州市经济和信息化局",
        "type": "政府",
        "level": "市",
        "parent": "达州市人民政府",
        "location": "达州市",
    },
    {
        "id": 9,
        "name": "达县（2000年前）",
        "type": "政府",
        "level": "县",
        "parent": "达州市",
        "location": "达州市",
    },
    {
        "id": 10,
        "name": "通川区人民政府",
        "type": "政府",
        "level": "县",
        "parent": "达州市人民政府",
        "location": "达州市通川区",
    },
    {
        "id": 11,
        "name": "达州市教育局",
        "type": "政府",
        "level": "市",
        "parent": "达州市人民政府",
        "location": "达州市",
    },
    {
        "id": 12,
        "name": "开江县纪委",
        "type": "政府",
        "level": "县",
        "parent": "开江县",
        "location": "开江县",
    },
    {
        "id": 13,
        "name": "达州市纪委",
        "type": "政府",
        "level": "市",
        "parent": "达州市",
        "location": "达州市",
    },
    {
        "id": 14,
        "name": "大竹县人民检察院",
        "type": "政府",
        "level": "县",
        "parent": "大竹县",
        "location": "大竹县",
    },
]

positions = [
    # 杨勇 — 县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "达州市人民政府副市长兼宣汉县委书记",
        "start": "2025-12",
        "end": "present",
        "rank": "副厅级",
        "note": "2025年12月29日被任命为达州市人民政府副市长，仍兼任宣汉县委书记",
    },
    {
        "person_id": 1,
        "org_id": 1,
        "title": "宣汉县委书记，一级调研员",
        "start": "2024-09",
        "end": "2025-12",
        "rank": "正处级",
        "note": "晋升一级调研员",
    },
    {
        "person_id": 1,
        "org_id": 1,
        "title": "宣汉县委书记",
        "start": "2024-01",
        "end": "2024-09",
        "rank": "正处级",
        "note": "任宣汉县委书记",
    },
    {
        "person_id": 1,
        "org_id": 8,
        "title": "达州市经济和信息化局党组书记、局长",
        "start": "2022-05",
        "end": "2024-01",
        "rank": "正处级",
    },
    {
        "person_id": 1,
        "org_id": 7,
        "title": "达州市农业农村局党组书记、局长兼市农科院党委书记",
        "start": "2020-04",
        "end": "2022-05",
        "rank": "正处级",
    },
    {
        "person_id": 1,
        "org_id": 7,
        "title": "达州市农业农村局党组书记、局长",
        "start": "2020-03",
        "end": "2020-04",
        "rank": "正处级",
    },
    {
        "person_id": 1,
        "org_id": 6,
        "title": "达州经济开发区党工委副书记、管委会主任",
        "start": "2019-01",
        "end": "2020-03",
        "rank": "正处级",
    },
    {
        "person_id": 1,
        "org_id": 6,
        "title": "达州经济开发区党工委副书记、管委会常务副主任",
        "start": "2017-09",
        "end": "2019-01",
        "rank": "副处级",
    },
    {
        "person_id": 1,
        "org_id": 6,
        "title": "达州经济开发区党工委副书记、管委会副主任",
        "start": "2016-01",
        "end": "2017-09",
        "rank": "副处级",
    },
    {
        "person_id": 1,
        "org_id": 10,
        "title": "达川区人民政府副区长",
        "start": "2013-09",
        "end": "2016-01",
        "rank": "副处级",
    },
    {
        "person_id": 1,
        "org_id": 9,
        "title": "达县人民政府党组成员、副县长",
        "start": "2012-01",
        "end": "2013-09",
        "rank": "副处级",
    },
    {
        "person_id": 1,
        "org_id": 9,
        "title": "达县人民政府党组成员、达县县委办公室主任",
        "start": "2011-10",
        "end": "2012-01",
        "rank": "正科级",
    },
    {
        "person_id": 1,
        "org_id": 9,
        "title": "达县县委办公室主任",
        "start": "2009-11",
        "end": "2011-10",
        "rank": "正科级",
    },
    {
        "person_id": 1,
        "org_id": 9,
        "title": "达县石梯镇党委书记、人大主席",
        "start": "2008-10",
        "end": "2009-11",
        "rank": "正科级",
    },
    {
        "person_id": 1,
        "org_id": 9,
        "title": "达县人民政府办公室副主任、达县人民政府督查室主任",
        "start": "2007-06",
        "end": "2008-10",
        "rank": "副科级",
    },
    {
        "person_id": 1,
        "org_id": 9,
        "title": "达县人民政府办公室副主任",
        "start": "2007-03",
        "end": "2007-06",
        "rank": "副科级",
    },
    {
        "person_id": 1,
        "org_id": 9,
        "title": "达县人民政府督查室主任",
        "start": "2003-04",
        "end": "2007-03",
        "rank": "副科级",
    },
    {
        "person_id": 1,
        "org_id": 9,
        "title": "达县人民政府办公室工作",
        "start": "1998-10",
        "end": "2003-04",
    },
    {
        "person_id": 1,
        "org_id": 9,
        "title": "达县林业局办公室主任、团总支书记",
        "start": "1996-02",
        "end": "1998-10",
    },
    {
        "person_id": 1,
        "org_id": 9,
        "title": "达县西山林场办公室主任、副场长",
        "start": "1991-09",
        "end": "1996-02",
    },
    # 陈军 — 县长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "宣汉县委副书记、县长，一级调研员",
        "start": "2022-11",
        "end": "present",
        "rank": "正处级",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "宣汉县委副书记、县长",
        "start": "2021-09",
        "end": "2022-11",
        "rank": "正处级",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "宣汉县委副书记、副县长、代县长",
        "start": "2021-07",
        "end": "2021-09",
        "rank": "正处级",
    },
    {
        "person_id": 2,
        "org_id": 11,
        "title": "达州市教育局党委书记、局长，市委教育工委书记（兼）",
        "start": "2019-01",
        "end": "2021-07",
        "rank": "正处级",
    },
    {
        "person_id": 2,
        "org_id": 10,
        "title": "通川区委副书记",
        "start": "2017-08",
        "end": "2019-01",
        "rank": "副处级",
    },
    {
        "person_id": 2,
        "org_id": 10,
        "title": "通川区委常委、常务副区长",
        "start": "2016-09",
        "end": "2017-08",
        "rank": "副处级",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "茂县县委常委、常务副县长（援藏）",
        "start": "2014-08",
        "end": "2016-09",
        "rank": "副处级",
    },
    {
        "person_id": 2,
        "org_id": 4,
        "title": "达州市人民政府办公室党组成员、副主任",
        "start": "2010-10",
        "end": "2014-08",
        "rank": "副处级",
    },
    {
        "person_id": 2,
        "org_id": 4,
        "title": "达州市人民政府办公室秘书四科科长",
        "start": "2007-08",
        "end": "2010-10",
        "rank": "正科级",
    },
    {
        "person_id": 2,
        "org_id": 4,
        "title": "达州市人民政府办公室秘书四科副科长、主任科员",
        "start": "2006-11",
        "end": "2007-08",
        "rank": "副科级",
    },
    {
        "person_id": 2,
        "org_id": 4,
        "title": "达州市人民政府办公室工作",
        "start": "2006-08",
        "end": "2006-11",
    },
    {
        "person_id": 2,
        "org_id": 12,
        "title": "开江县委政研室主任",
        "start": "2006-02",
        "end": "2006-08",
        "rank": "正科级",
    },
    {
        "person_id": 2,
        "org_id": 12,
        "title": "开江县委、县人民政府督查室副主任",
        "start": "2004-09",
        "end": "2006-02",
        "rank": "副科级",
    },
    {
        "person_id": 2,
        "org_id": 12,
        "title": "开江县纪委执法监察纠风室主任",
        "start": "2003-04",
        "end": "2004-09",
    },
    {
        "person_id": 2,
        "org_id": 12,
        "title": "开江县纪委执法监察室主任",
        "start": "2002-08",
        "end": "2003-04",
    },
    {
        "person_id": 2,
        "org_id": 13,
        "title": "达州市纪委电教中心工作",
        "start": "2000-08",
        "end": "2002-04",
    },
    {
        "person_id": 2,
        "org_id": 12,
        "title": "开江县纪委工作",
        "start": "1998-08",
        "end": "2000-08",
    },
    {
        "person_id": 2,
        "org_id": 12,
        "title": "开江县沙坝场乡中心校教师（借调县纪委）",
        "start": "1996-08",
        "end": "1998-08",
    },
    # 李静 — 常务副县长
    {
        "person_id": 5,
        "org_id": 2,
        "title": "县委常委、常务副县长",
        "start": "2024-04",
        "end": "present",
        "rank": "副处级",
    },
    {
        "person_id": 5,
        "org_id": 2,
        "title": "县委常委、副县长",
        "start": "2021-09",
        "end": "2024-04",
        "rank": "副处级",
    },
    {
        "person_id": 5,
        "org_id": 2,
        "title": "县委常委、县政府党组成员",
        "start": "2021-08",
        "end": "2021-09",
        "rank": "副处级",
    },
    {
        "person_id": 5,
        "org_id": 4,
        "title": "达州市政协办公室副主任（挂职达州高新区）",
        "start": "2020-09",
        "end": "2021-08",
        "rank": "副处级",
    },
    {
        "person_id": 5,
        "org_id": 4,
        "title": "达州市政协办公室副主任",
        "start": "2019-09",
        "end": "2020-09",
        "rank": "副处级",
    },
    {
        "person_id": 5,
        "org_id": 4,
        "title": "达州市政协办公室副主任（挂职省财政厅）",
        "start": "2019-03",
        "end": "2019-09",
        "rank": "副处级",
    },
    {
        "person_id": 5,
        "org_id": 4,
        "title": "达州市政协办公室秘书科科长",
        "start": "2018-05",
        "end": "2019-03",
        "rank": "正科级",
    },
    {
        "person_id": 5,
        "org_id": 4,
        "title": "达州市政协办公室人事科科长",
        "start": "2014-04",
        "end": "2018-05",
        "rank": "正科级",
    },
    {
        "person_id": 5,
        "org_id": 4,
        "title": "达州市政协办公室秘书科副科长",
        "start": "2012-12",
        "end": "2014-04",
        "rank": "副科级",
    },
    # 陈刚 — 副县长/公安局长
    {
        "person_id": 9,
        "org_id": 3,
        "title": "宣汉县副县长、公安局长",
        "start": "2021-08",
        "end": "present",
        "rank": "副处级",
    },
    {
        "person_id": 9,
        "org_id": 14,
        "title": "大竹县人民检察院党组书记、检察长",
        "start": "2016-02",
        "end": "2021-08",
        "rank": "副处级",
    },
    {
        "person_id": 9,
        "org_id": 14,
        "title": "大竹县人民检察院党组书记、代检察长",
        "start": "2015-12",
        "end": "2016-02",
        "rank": "副处级",
    },
    {
        "person_id": 9,
        "org_id": 12,
        "title": "开江县人民检察院副检察长",
        "start": "2007-11",
        "end": "2015-12",
        "rank": "正科级",
    },
    {
        "person_id": 9,
        "org_id": 12,
        "title": "开江县城市管理联合执法大队大队长",
        "start": "2005-06",
        "end": "2007-11",
    },
    {
        "person_id": 9,
        "org_id": 12,
        "title": "开江县公安局刑警大队副大队长",
        "start": "1997-08",
        "end": "2005-06",
    },
    # 胡锐 — 副县长（帝国理工博士）
    {
        "person_id": 10,
        "org_id": 2,
        "title": "副县长",
        "start": "2023-04",
        "end": "present",
        "rank": "副处级",
    },
    # 林兰忻 — 副县长（中科院博士）
    {
        "person_id": 11,
        "org_id": 2,
        "title": "副县长",
        "start": "2024-03",
        "end": "present",
        "rank": "副处级",
    },
    # 周颜 — 副县长（2026新任）
    {
        "person_id": 12,
        "org_id": 2,
        "title": "副县长",
        "start": "2026-01",
        "end": "present",
        "rank": "副处级",
    },
    # 李京晏 — 县委常委、副县长（中信背景）
    {
        "person_id": 8,
        "org_id": 2,
        "title": "县委常委、副县长",
        "start": "2026-06",
        "end": "present",
        "rank": "副处级",
    },
]

relationships = [
    # 杨勇 ↔ 陈军：上下级关系（县委书记-县长搭档）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "杨勇任宣汉县委书记、陈军任宣汉县委副书记、县长，两人为党政主要领导搭档",
        "overlap_org": "中共宣汉县委员会/宣汉县人民政府",
        "overlap_period": "2024-01至今",
        "strength": "strong",
    },
    # 杨勇 ↔ 李静：上下级关系
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "杨勇任县委书记期间，李静任县委常委、常务副县长",
        "overlap_org": "宣汉县人民政府",
        "overlap_period": "2024-01至今",
        "strength": "strong",
    },
    # 陈军 ↔ 李静：上下级
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "陈军任县长、李静任常务副县长，为政府班子正副职搭档",
        "overlap_org": "宣汉县人民政府",
        "overlap_period": "2021-09至今",
        "strength": "strong",
    },
    # 杨勇 → 冯永刚：前后任
    {
        "person_a": 1,
        "person_b": 13,
        "type": "predecessor_successor",
        "context": "冯永刚任宣汉县委书记至2024年初，杨勇继任宣汉县委书记",
        "overlap_org": "中共宣汉县委员会",
        "overlap_period": "2024",
        "strength": "strong",
    },
    # 陈军 → 陈刚：同姓不宗，工作关系（公安归口县政府）
    {
        "person_a": 2,
        "person_b": 9,
        "type": "overlap",
        "context": "陈军任县长、陈刚任副县长/公安局长，为同一政府班子",
        "overlap_org": "宣汉县人民政府",
        "overlap_period": "2021-08至今",
        "strength": "medium",
    },
    # 杨勇 ↔ 胡锐：上下级
    {
        "person_a": 1,
        "person_b": 10,
        "type": "overlap",
        "context": "杨勇任县委书记、胡锐任副县长",
        "overlap_org": "宣汉县人民政府",
        "overlap_period": "2024-01至今",
        "strength": "medium",
    },
    # 李京晏 ↔ 陈军：上下级（新到岗）
    {
        "person_a": 8,
        "person_b": 2,
        "type": "overlap",
        "context": "李京晏2026年6月到任县委常委、副县长，与县长陈军在同一班子",
        "overlap_org": "宣汉县人民政府",
        "overlap_period": "2026-06至今",
        "strength": "medium",
    },
    # 周颜 ↔ 陈军：上下级（周颜2026年新任副县长）
    {
        "person_a": 12,
        "person_b": 2,
        "type": "overlap",
        "context": "周颜2026年1月任副县长，为陈军下属",
        "overlap_org": "宣汉县人民政府",
        "overlap_period": "2026-01至今",
        "strength": "medium",
    },
    # 陈刚 ↔ 周颜（同城工作）
    {
        "person_a": 9,
        "person_b": 12,
        "type": "overlap",
        "context": "陈刚与周颜均为宣汉县副县长，同一政府班子",
        "overlap_org": "宣汉县人民政府",
        "overlap_period": "2026-01至今",
        "strength": "medium",
    },
    # 潘攀 ↔ 李京晏（都是县委常委、副县长）
    {
        "person_a": 7,
        "person_b": 8,
        "type": "overlap",
        "context": "潘攀与李京晏均为县委常委、副县长",
        "overlap_org": "宣汉县人民政府",
        "overlap_period": "2026-03至今",
        "strength": "medium",
    },
]

# ── Builder ────────────────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
        CREATE TABLE persons (
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
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p["id"], p["name"], p.get("gender"), p.get("ethnicity"), p.get("birth"), p.get("birthplace"),
             p.get("education"), p.get("party_join"), p.get("work_start"), p.get("current_post"), p.get("current_org"), p.get("source")),
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o["type"], o["level"], o.get("parent"), o.get("location")),
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos.get("start"), pos.get("end"), pos.get("rank"), pos.get("note")),
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org"), r.get("overlap_period"), r.get("strength")),
        )

    conn.commit()
    conn.close()
    print(f"  DB  →  {DB_PATH}")
    print(f"        Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")


def build_gexf():
    now = "2026-07-28"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append(f'    <description>宣汉县（达州市）领导班子关系网络，数据截至{now}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person node colors
    person_colors = {
        1: ("255,50,50", 20.0),      # 杨勇 - 县委书记 = red
        2: ("50,100,255", 20.0),     # 陈军 - 县长 = blue
        3: ("100,100,100", 12.0),    # 杨轶
        4: ("100,100,100", 12.0),    # 吴中凡
        5: ("50,100,255", 12.0),     # 李静 - 常务副县长 = blue
        6: ("50,100,255", 12.0),     # 叶仙富 (挂职)
        7: ("50,100,255", 12.0),     # 潘攀
        8: ("50,100,255", 12.0),     # 李京晏
        9: ("50,100,255", 12.0),     # 陈刚 - 副县长
        10: ("50,100,255", 12.0),    # 胡锐
        11: ("50,100,255", 12.0),    # 林兰忻
        12: ("50,100,255", 12.0),    # 周颜
        13: ("100,100,100", 12.0),   # 冯永刚 (前任)
        14: ("100,100,100", 12.0),   # 唐廷教 (前任)
    }

    for p in persons:
        pid = p["id"]
        color, size = person_colors.get(pid, ("100,100,100", 12.0))
        role = "party_secretary" if pid == 1 else "county_mayor" if pid == 2 else "deputy"
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        r, g, b = color.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append('      </node>')

    # Organization node colors by type
    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "开发区": ("200,255,200", 8.0),
    }
    for o in organizations:
        color, size = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{o["type"]}"/>')
        lines.append('        </attvalues>')
        r, g, b = color.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at) — for current key positions
    person_current_orgs = []
    for p in persons:
        if p.get("current_org") and p["current_post"]:
            org_match = [o for o in organizations if o["name"] in p["current_org"] or p["current_org"] in o["name"]]
            if org_match:
                person_current_orgs.append((p["id"], org_match[0]["id"], p["current_post"]))

    for pid, oid, title in person_current_orgs:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        strength_weight = {"strong": 2.0, "medium": 1.5, "weak": 1.0}
        w = strength_weight.get(r.get("strength", "weak"), 1.0)
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{r["type"]}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{r.get("strength", "weak")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF  ->  {GEXF_PATH}")


def main():
    print(f"宣汉县（达州市）领导班子关系网络 - {AS_OF}")
    print(f"源数据：宣汉县人民政府官网")
    print(f"=" * 50)
    build_db()
    build_gexf()
    print(f"=" * 50)
    print("完成。数据说明：")
    print(f"  - 核心人物 杨勇、陈军简历来源于政府官网")
    print(f"  - 副书记杨轶、吴中凡详细信息待补充")
    print(f"  - 前任县委书记冯永刚、唐廷教为已知信息")
    print(f"  - 部分常委（组织部长、宣传部长等）需进一步调研")


if __name__ == "__main__":
    main()