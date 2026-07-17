#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Hunan Province Governor Mao Weiming's network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/hunan_gov_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/hunan_gov_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Leader: Governor of Hunan Province ──
    {"id": 1, "name": "毛伟明", "gender": "男", "ethnicity": "汉族",
     "birth": "1961-05", "birthplace": "浙江衢州", "education": "浙江大学化学工程系化工机械专业，工学学士",
     "party_join": "1985-09", "work_start": "1982-08",
     "current_post": "湖南省省长", "current_org": "湖南省人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E6%AF%9B%E4%BC%9F%E6%98%8E"},
    # ── Party Secretary (Superior/Partner) ──
    {"id": 2, "name": "沈晓明", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-05", "birthplace": "浙江上虞", "education": "温州医学院儿科系本科(1979-1984)/硕士(1984-1987)，上海第二医科大学儿科学博士(1988-1991)",
     "party_join": "1984-08", "work_start": "1987-07",
     "current_post": "湖南省委书记、省人大常委会主任", "current_org": "中共湖南省委",
     "source": "https://zh.wikipedia.org/wiki/%E6%B2%88%E6%99%93%E6%98%8E"},
    # ── Shen Xiaoming's predecessor in Hunan (张庆伟) ──
    {"id": 18, "name": "张庆伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1961-11", "birthplace": "吉林吉林", "education": "西北工业大学飞机设计专业硕士，北京航空航天大学管理科学博士",
     "party_join": "1992-12", "work_start": "1982-08",
     "current_post": "全国人大常委会副委员长", "current_org": "全国人大常委会",
     "source": "https://zh.wikipedia.org/wiki/%E5%BC%A0%E5%BA%86%E4%BC%9F"},
    # ── Shen Xiaoming's Hainan predecessor and successor ──
    {"id": 19, "name": "刘赐贵", "gender": "男", "ethnicity": "汉族",
     "birth": "1955-09", "birthplace": "福建惠安", "education": "中央党校在职研究生",
     "party_join": "中共党员", "work_start": "1973-07",
     "current_post": "全国政协港澳台侨委员会主任", "current_org": "全国政协",
     "source": "https://zh.wikipedia.org/wiki/%E5%88%98%E8%B5%90%E8%B4%B5"},
    {"id": 20, "name": "冯飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1962-12", "birthplace": "江西都昌", "education": "天津大学自动化系工学博士",
     "party_join": "中共党员", "work_start": "1985-07",
     "current_post": "海南省委书记", "current_org": "中共海南省委",
     "source": "https://zh.wikipedia.org/wiki/%E5%86%AF%E9%A3%9E"},
    # ── Additional standing committee members with more detail ──
    {"id": 21, "name": "隋忠诚", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-06", "birthplace": "吉林双阳", "education": "在职研究生学历，经济学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省委统战部部长", "current_org": "中共湖南省委",
     "source": "https://zh.wikipedia.org/wiki/%E9%9A%8B%E5%BF%A0%E8%AF%9A"},
    {"id": 22, "name": "魏建锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-04", "birthplace": "河南禹州", "education": "研究生学历，工学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省纪委书记", "current_org": "中共湖南省纪律检查委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%AD%8F%E5%BB%BA%E9%94%8B"},
    {"id": 23, "name": "刘红兵", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-01", "birthplace": "安徽砀山", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省委宣传部部长", "current_org": "中共湖南省委宣传部",
     "source": "https://zh.wikipedia.org/wiki/%E5%88%98%E7%BA%A2%E5%85%B5"},
    {"id": 24, "name": "郭灵计", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-07", "birthplace": "山西隰县", "education": "中央党校研究生，公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省委组织部部长", "current_org": "中共湖南省委组织部",
     "source": "https://zh.wikipedia.org/wiki/%E9%83%AD%E7%81%B5%E8%AE%A1"},
    {"id": 25, "name": "王俊寿", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-01", "birthplace": "山西阳泉", "education": "研究生学历，经济学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省委秘书长、副省长", "current_org": "中共湖南省委",
     "source": "https://zh.wikipedia.org/wiki/%E7%8E%8B%E4%BF%8A%E5%AF%BF"},
    # ── Predecessor: Previous Governor ──
    {"id": 3, "name": "许达哲", "gender": "男", "ethnicity": "汉族",
     "birth": "1956-09", "birthplace": "湖南浏阳", "education": "哈尔滨工业大学机械制造专业，工学硕士",
     "party_join": "1982-01", "work_start": "1975-12",
     "current_post": "曾任湖南省委书记（2021-2023）", "current_org": "中共湖南省委",
     "source": "https://zh.wikipedia.org/wiki/%E8%AE%B8%E8%BE%BE%E5%93%B2"},
    # ── Predecessor Governor before Xu ──
    {"id": 4, "name": "杜家毫", "gender": "男", "ethnicity": "汉族",
     "birth": "1955-07", "birthplace": "浙江鄞县", "education": "华东师范大学中文系，大学学历",
     "party_join": "1973-12", "work_start": "1973-03",
     "current_post": "曾任湖南省委书记（2016-2020）", "current_org": "中共湖南省委",
     "source": "https://zh.wikipedia.org/wiki/%E6%9D%9C%E5%AE%B6%E6%AF%AB"},
    # ── Executive Vice Governor (常务副省长) ──
    {"id": 5, "name": "王道席", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-12", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省常务副省长", "current_org": "湖南省人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E7%8E%8B%E9%81%93%E5%B8%AD"},
    # ── Vice Governor (公安厅厅长) ──
    {"id": 6, "name": "王一鸥", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-10", "birthplace": "", "education": "研究生学历，工商管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省副省长、省公安厅厅长", "current_org": "湖南省人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E7%8E%8B%E4%B8%80%E9%B8%A5"},
    # ── Vice Governor (non-CCP) ──
    {"id": 7, "name": "蒋涤非", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-10", "birthplace": "", "education": "研究生学历，工学博士",
     "party_join": "民革党员", "work_start": "",
     "current_post": "湖南省副省长", "current_org": "湖南省人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E8%92%8B%E6%B6%A4%E9%9D%9E"},
    # ── Vice Governor (Changsha Party Secretary) ──
    {"id": 8, "name": "陈竞", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-02", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省副省长、长沙市委书记", "current_org": "中共长沙市委",
     "source": "https://zh.wikipedia.org/wiki/%E9%99%88%E7%AB%9E_(1971%E5%B9%B4)"},
    # ── Vice Governor ──
    {"id": 9, "name": "余红胜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省副省长", "current_org": "湖南省人民政府",
     "source": ""},
    # ── Vice Governor ──
    {"id": 10, "name": "刘扬", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-01", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省副省长", "current_org": "湖南省人民政府",
     "source": ""},
    # ── Party Secretary deputy (省委副书记) ──
    {"id": 11, "name": "谢卫江", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-01", "birthplace": "", "education": "研究生学历，工学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省委副书记、岳阳市委书记", "current_org": "中共湖南省委",
     "source": "https://zh.wikipedia.org/wiki/%E8%B0%A2%E5%8D%AB%E6%B1%9F"},
]

organizations = [
    {"id": 1, "name": "湖南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "长沙"},
    {"id": 2, "name": "中共湖南省委", "type": "党委", "level": "省级", "parent": "", "location": "长沙"},
    {"id": 3, "name": "中共湖南省纪律检查委员会", "type": "党委", "level": "省级", "parent": "中共湖南省委", "location": "长沙"},
    {"id": 4, "name": "湖南省委统战部", "type": "党委", "level": "省级", "parent": "中共湖南省委", "location": "长沙"},
    {"id": 5, "name": "湖南省委宣传部", "type": "党委", "level": "省级", "parent": "中共湖南省委", "location": "长沙"},
    {"id": 6, "name": "湖南省委组织部", "type": "党委", "level": "省级", "parent": "中共湖南省委", "location": "长沙"},
    {"id": 7, "name": "湖南省军区", "type": "事业单位", "level": "省级", "parent": "", "location": "长沙"},
    {"id": 8, "name": "湖南省公安厅", "type": "政府", "level": "省级", "parent": "湖南省人民政府", "location": "长沙"},
    {"id": 9, "name": "中共长沙市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "长沙"},
    {"id": 10, "name": "国家电网有限公司", "type": "事业单位", "level": "央企", "parent": "", "location": "北京"},
    {"id": 11, "name": "中华人民共和国工业和信息化部", "type": "政府", "level": "中央部委", "parent": "", "location": "北京"},
    {"id": 12, "name": "江苏省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "南京"},
    {"id": 13, "name": "江苏省发展和改革委员会", "type": "政府", "level": "省级", "parent": "江苏省人民政府", "location": "南京"},
    {"id": 14, "name": "泰州市人民政府", "type": "政府", "level": "地市级", "parent": "江苏省人民政府", "location": "泰州"},
    {"id": 15, "name": "中共武进市委", "type": "党委", "level": "地市级", "parent": "", "location": "常州"},
    {"id": 16, "name": "武进市人民政府", "type": "政府", "level": "地市级", "parent": "", "location": "常州"},
    {"id": 17, "name": "常州绝缘材料总厂", "type": "事业单位", "level": "企业", "parent": "", "location": "常州"},
    {"id": 18, "name": "江西省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "南昌"},
    {"id": 19, "name": "海南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "海口"},
    {"id": 20, "name": "中华人民共和国教育部", "type": "政府", "level": "中央部委", "parent": "", "location": "北京"},
    {"id": 21, "name": "中共上海市委", "type": "党委", "level": "省级", "parent": "", "location": "上海"},
    {"id": 22, "name": "上海市浦东新区区委", "type": "党委", "level": "地市级", "parent": "中共上海市委", "location": "上海"},
    {"id": 23, "name": "中共岳阳市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "岳阳"},
    {"id": 24, "name": "全国人大常委会", "type": "政府", "level": "中央", "parent": "", "location": "北京"},
    {"id": 25, "name": "全国政协", "type": "政府", "level": "中央", "parent": "", "location": "北京"},
    {"id": 26, "name": "中共海南省委", "type": "党委", "level": "省级", "parent": "", "location": "海口"},
    {"id": 27, "name": "浦东新区区委", "type": "党委", "level": "地市级", "parent": "中共上海市委", "location": "上海"},
]

positions = [
    # ── Mao Weiming's complete career ──
    {"id": 1, "person_id": 1, "org_id": 17, "title": "常州绝缘材料总厂车间主任、厂长助理、副厂长、厂长、党委书记",
     "start": "1982-08", "end": "1993", "rank": "企业", "note": "第一份工作，从车间主任升至厂长"},
    {"id": 2, "person_id": 1, "org_id": 15, "title": "中共武进市委副书记、副市长",
     "start": "1993", "end": "1998-10", "rank": "副厅级", "note": "转入地方党政系统"},
    {"id": 3, "person_id": 1, "org_id": 16, "title": "武进市人民政府代市长→市长",
     "start": "1998-10", "end": "2001-11", "rank": "正厅级", "note": "1998年10月代理，1999年1月正式当选"},
    {"id": 4, "person_id": 1, "org_id": 15, "title": "中共武进市委书记",
     "start": "2001-02", "end": "2001-11", "rank": "正厅级", "note": ""},
    {"id": 5, "person_id": 1, "org_id": 14, "title": "泰州市人民政府代市长→市长",
     "start": "2003-04", "end": "2006-01", "rank": "正厅级", "note": "2003年5月正式当选"},
    {"id": 6, "person_id": 1, "org_id": 13, "title": "江苏省发展和改革委员会主任",
     "start": "2006-01", "end": "2011-11", "rank": "正厅级", "note": ""},
    {"id": 7, "person_id": 1, "org_id": 12, "title": "江苏省人民政府秘书长",
     "start": "2011-11", "end": "2013-03", "rank": "副部级", "note": ""},
    {"id": 8, "person_id": 1, "org_id": 12, "title": "江苏省副省长",
     "start": "2013-01", "end": "2013-10", "rank": "副部级", "note": ""},
    {"id": 9, "person_id": 1, "org_id": 11, "title": "工业和信息化部副部长",
     "start": "2013-10", "end": "2015-07", "rank": "副部级", "note": "2013年11月正式任命"},
    {"id": 10, "person_id": 1, "org_id": 18, "title": "江西省委常委、常务副省长",
     "start": "2015-08", "end": "2020-01", "rank": "副部级", "note": "2015年9月正式就任常务副省长"},
    {"id": 11, "person_id": 1, "org_id": 10, "title": "国家电网有限公司董事长、党组书记",
     "start": "2020-01", "end": "2020-11", "rank": "副部级", "note": "央企一把手"},
    {"id": 12, "person_id": 1, "org_id": 1, "title": "湖南省代省长→省长",
     "start": "2020-11", "end": "", "rank": "正部级", "note": "2020年11月任代省长，2021年1月正式当选"},
    {"id": 13, "person_id": 1, "org_id": 2, "title": "湖南省委副书记",
     "start": "2020-11", "end": "", "rank": "正部级", "note": "兼任"},

    # ── Shen Xiaoming's COMPLETE career timeline (from earliest to latest) ──
    {"id": 14, "person_id": 2, "org_id": 2, "title": "湖南省委书记、省人大常委会主任",
     "start": "2023-03", "end": "", "rank": "正部级", "note": "2023年3月接替张庆伟；2024年1月当选省人大常委会主任"},
    {"id": 15, "person_id": 2, "org_id": 19, "title": "海南省委书记、省人大常委会主任",
     "start": "2020-12", "end": "2023-03", "rank": "正部级", "note": "2020年12月接替刘赐贵；2021年1月当选省人大常委会主任"},
    {"id": 16, "person_id": 2, "org_id": 19, "title": "海南省省长",
     "start": "2017-04", "end": "2020-12", "rank": "正部级", "note": "2017年4月任代省长，5月正式当选；从副部级直接升任正部级"},
    {"id": 17, "person_id": 2, "org_id": 20, "title": "教育部副部长、党组副书记",
     "start": "2016-09", "end": "2017-03", "rank": "副部级", "note": "约6个月过渡性任职"},
    {"id": 18, "person_id": 2, "org_id": 22, "title": "上海市委常委、浦东新区区委书记",
     "start": "2013-05", "end": "2016-09", "rank": "副部级", "note": "兼上海自贸区管委会主任(2015-2016)"},
    {"id": 19, "person_id": 2, "org_id": 21, "title": "上海市副市长",
     "start": "2008-01", "end": "2013-05", "rank": "副部级", "note": "兼张江高新区管委会主任(2010-2013)、红十字会会长(2009-2013)"},
    {"id": 40, "person_id": 2, "org_id": 21, "title": "上海市教委主任、市科教工作党委副书记",
     "start": "2006", "end": "2008-01", "rank": "正厅级", "note": "从高校转入政界"},
    {"id": 41, "person_id": 2, "org_id": 21, "title": "上海交通大学常务副校长、医学院院长",
     "start": "2005", "end": "2006", "rank": "正厅级", "note": "上海第二医科大学并入交大后任职"},
    {"id": 42, "person_id": 2, "org_id": 21, "title": "上海第二医科大学校长",
     "start": "2003", "end": "2005", "rank": "正厅级", "note": "中国最年轻的医科大学校长之一"},
    {"id": 43, "person_id": 2, "org_id": 21, "title": "上海第二医科大学附属新华医院院长",
     "start": "2001", "end": "2003", "rank": "正处级", "note": "兼上海儿童医学中心院长"},
    {"id": 44, "person_id": 2, "org_id": 21, "title": "上海第二医科大学附属新华医院副院长",
     "start": "1998", "end": "2001", "rank": "副处级", "note": "兼上海儿童医学中心院长"},
    {"id": 45, "person_id": 2, "org_id": 21, "title": "上海儿童医学中心常务副院长",
     "start": "1996", "end": "1998", "rank": "副处级", "note": "1994-1996美国爱因斯坦医学院博士后"},
    {"id": 46, "person_id": 2, "org_id": 21, "title": "上海第二医科大学新华医院主治医师、副研究员",
     "start": "1991", "end": "1994", "rank": "医师", "note": ""},
    {"id": 47, "person_id": 2, "org_id": 21, "title": "上海第二医科大学儿科学博士研究生",
     "start": "1988", "end": "1991", "rank": "学生", "note": "儿童保健学专业"},
    {"id": 48, "person_id": 2, "org_id": 21, "title": "浙江医科大学附属一院住院医师、温州医学院助教",
     "start": "1987", "end": "1988", "rank": "医师", "note": "毕业后第一份工作"},

    # ── Xu Dazhe ──
    {"id": 20, "person_id": 3, "org_id": 2, "title": "湖南省委书记",
     "start": "2021-01", "end": "2023-03", "rank": "正部级", "note": ""},
    {"id": 21, "person_id": 3, "org_id": 1, "title": "湖南省省长",
     "start": "2016-09", "end": "2020-11", "rank": "正部级", "note": ""},

    # ── Du Jiahao ──
    {"id": 22, "person_id": 4, "org_id": 2, "title": "湖南省委书记",
     "start": "2016-09", "end": "2020-11", "rank": "正部级", "note": ""},
    {"id": 23, "person_id": 4, "org_id": 1, "title": "湖南省省长",
     "start": "2013-04", "end": "2016-09", "rank": "正部级", "note": ""},

    # ── Current leadership team positions ──
    {"id": 24, "person_id": 5, "org_id": 1, "title": "湖南省常务副省长",
     "start": "", "end": "", "rank": "副部级", "note": "省委常委"},
    {"id": 25, "person_id": 6, "org_id": 1, "title": "湖南省副省长",
     "start": "", "end": "", "rank": "副部级", "note": "兼省公安厅厅长"},
    {"id": 26, "person_id": 6, "org_id": 8, "title": "湖南省公安厅厅长",
     "start": "", "end": "", "rank": "正厅级", "note": ""},
    {"id": 27, "person_id": 7, "org_id": 1, "title": "湖南省副省长",
     "start": "", "end": "", "rank": "副部级", "note": "民革党员"},
    {"id": 28, "person_id": 8, "org_id": 9, "title": "长沙市委书记",
     "start": "", "end": "", "rank": "副部级", "note": "省委常委"},
    {"id": 29, "person_id": 8, "org_id": 1, "title": "湖南省副省长",
     "start": "", "end": "", "rank": "副部级", "note": ""},
    {"id": 30, "person_id": 9, "org_id": 1, "title": "湖南省副省长",
     "start": "", "end": "", "rank": "副部级", "note": ""},
    {"id": 31, "person_id": 10, "org_id": 1, "title": "湖南省副省长",
     "start": "", "end": "", "rank": "副部级", "note": ""},
    {"id": 32, "person_id": 11, "org_id": 2, "title": "湖南省委副书记",
     "start": "", "end": "", "rank": "副部级", "note": "兼岳阳市委书记"},
    {"id": 33, "person_id": 11, "org_id": 23, "title": "岳阳市委书记",
     "start": "", "end": "", "rank": "副部级", "note": "省委副书记兼任"},
    {"id": 34, "person_id": 12, "org_id": 4, "title": "湖南省委统战部部长",
     "start": "", "end": "", "rank": "副部级", "note": "省委常委"},
    {"id": 35, "person_id": 13, "org_id": 3, "title": "湖南省纪委书记",
     "start": "", "end": "", "rank": "副部级", "note": "省委常委"},
    {"id": 36, "person_id": 14, "org_id": 5, "title": "湖南省委宣传部部长",
     "start": "", "end": "", "rank": "副部级", "note": "省委常委"},
    {"id": 37, "person_id": 15, "org_id": 6, "title": "湖南省委组织部部长",
     "start": "", "end": "", "rank": "副部级", "note": "省委常委"},
    {"id": 38, "person_id": 16, "org_id": 7, "title": "湖南省军区政委",
     "start": "", "end": "", "rank": "正军级", "note": "省委常委"},
    {"id": 39, "person_id": 17, "org_id": 2, "title": "湖南省委秘书长",
     "start": "", "end": "", "rank": "副部级", "note": "省委常委"},
]

relationships = [
    # ── Mao Weiming's key relationships ──

    # With Shen Xiaoming (current boss - work together since 2023)
    {"id": 1, "person_a": 1, "person_b": 2, "type": "work_together",
     "context": "2023年起毛伟明（省长）与沈晓明（省委书记）搭班任职湖南省委",
     "overlap_org": "中共湖南省委/湖南省人民政府", "overlap_period": "2023-至今"},

    # With Xu Dazhe (predecessor as governor)
    {"id": 2, "person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "毛伟明接替许达哲任湖南省省长（许达哲升任省委书记）",
     "overlap_org": "湖南省人民政府/中共湖南省委", "overlap_period": "2020-2021"},

    # Both Zhejiang natives (Mao Quzhou, Shen Shangyu)
    {"id": 3, "person_a": 1, "person_b": 2, "type": "same_province",
     "context": "同为浙江籍高级干部（毛伟明浙江衢州人，沈晓明浙江上虞人）",
     "overlap_org": "", "overlap_period": ""},

    # With Du Jiahao (also Zhejiang native, predecessor chain)
    {"id": 4, "person_a": 1, "person_b": 4, "type": "same_province",
     "context": "同籍浙江（杜家毫浙江鄞县人），通过许达哲间接连接",
     "overlap_org": "", "overlap_period": ""},

    # Shen Xiaoming - Xu Dazhe (predecessor party secretary)
    {"id": 5, "person_a": 2, "person_b": 3, "type": "predecessor_successor",
     "context": "沈晓明接替许达哲任湖南省委书记",
     "overlap_org": "中共湖南省委", "overlap_period": "2023"},

    # Du Jiahao - Xu Dazhe
    {"id": 6, "person_a": 4, "person_b": 3, "type": "predecessor_successor",
     "context": "杜家毫任省委书记时，许达哲任省长，后许达哲接替杜家毫任书记",
     "overlap_org": "中共湖南省委", "overlap_period": "2016-2020"},

    # Mao - Vice Govs (work together)
    {"id": 7, "person_a": 1, "person_b": 5, "type": "work_together",
     "context": "王道席作为常务副省长协助毛伟明工作",
     "overlap_org": "湖南省人民政府", "overlap_period": ""},

    {"id": 8, "person_a": 1, "person_b": 6, "type": "work_together",
     "context": "王一鸥作为副省长协助毛伟明工作",
     "overlap_org": "湖南省人民政府", "overlap_period": ""},

    # Mao - from Jiangxi connection (Mao and Shen both worked in Jiangxi system)
    {"id": 9, "person_a": 1, "person_b": 2, "type": "cross_province",
     "context": "毛伟明曾任江西省常务副省长（2015-2020），沈晓明曾任海南省省长（2017-2020），两人在2017年后均为正部级官员，多有会议交集",
     "overlap_org": "", "overlap_period": ""},

    # Shen Xiaoming - Zhang Qingwei (predecessor as Hunan Party Secretary)
    {"id": 10, "person_a": 2, "person_b": 18, "type": "predecessor_successor",
     "context": "沈晓明2023年3月接替张庆伟任湖南省委书记（张升任全国人大常委会副委员长）",
     "overlap_org": "中共湖南省委", "overlap_period": "2023-03"},
    # Shen Xiaoming - Liu Cigui (predecessor as Hainan Party Secretary, former boss as Governor)
    {"id": 11, "person_a": 2, "person_b": 19, "type": "work_together",
     "context": "刘赐贵（海南省委书记）与沈晓明（海南省省长）搭班近4年（2017-2020）；后沈晓明接替刘赐贵任书记",
     "overlap_org": "中共海南省委/海南省人民政府", "overlap_period": "2017-2020"},
    # Shen Xiaoming - Feng Fei (successor as Hainan Party Secretary)
    {"id": 12, "person_a": 2, "person_b": 20, "type": "predecessor_successor",
     "context": "沈晓明调任湖南后冯飞于2023年3月接替其任海南省委书记（冯此前任海南省长）",
     "overlap_org": "中共海南省委", "overlap_period": "2023"},
    # Zhang Qingwei - Xu Dazhe (both aerospace system)
    {"id": 13, "person_a": 18, "person_b": 3, "type": "same_system",
     "context": "张庆伟（航天科技集团总经理/COMAC董事长）与许达哲（航天科工集团总经理/航天科技董事长）均长期在航天系统工作，有业界交集",
     "overlap_org": "", "overlap_period": ""},
]


# ── BUILD SQLite ────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
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
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT OR REPLACE INTO positions
            VALUES (?,?,?,?,?,?,?,?)""",
            (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT OR REPLACE INTO relationships
            VALUES (?,?,?,?,?,?,?)""",
            (r["id"], r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✓ SQLite DB created: {DB_PATH}")


# ── BUILD GEXF ──────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    name = p["name"]
    role = p.get("current_post", "")
    if "书记" in role and "省长" not in role:
        return "255,50,50"  # Red for party secretaries
    if "省长" in role or "市长" in role or "县长" in role:
        return "50,100,255"  # Blue for government leaders
    if "纪委书记" in role or "纪检" in role:
        return "255,165,0"  # Orange for discipline
    if "副省长" in role:
        return "50,100,255"  # Blue for government
    return "100,100,100"  # Grey

def org_color(o):
    t = o.get("type", "")
    if "党委" in t: return "255,200,200"
    if "政府" in t: return "200,200,255"
    if "开发区" in t: return "200,255,200"
    if "事业" in t: return "220,220,220"
    return "200,200,200"

def is_top_leader(p):
    role = p.get("current_post", "")
    return "省长" in role or "书记" in role

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>湖南省领导班子工作关系网络 - 省长毛伟明</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('      <attribute id="4" title="education" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("education",""))}"/>')
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
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Worked-at edges (person -> organization)
    for pos in positions:
        eid += 1
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = pos["title"][:40] + ("…" if len(pos["title"]) > 40 else "")
        weight = "1.0"
        start = esc(pos.get("start", "") or "")
        end = esc(pos.get("end", "") or "")
        note = esc(pos.get("note", "") or "")
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="({start} - {end}) {note}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges (person <-> person)
    for r in relationships:
        eid += 1
        weight = "2.0"  # thicker for person-person
        context = esc(r.get("context", "") or "")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{context}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ GEXF graph created: {GEXF_PATH}")


# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_db()
    build_gexf()
    print(f"\n  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print("✓ Done")
