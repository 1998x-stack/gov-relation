#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 长沙市领导班子 (Changsha City Leadership Network).
Investigation date: 2026-07-14
Current 长沙市委书记: 陈竞 (as of 2026-06-12)
"""

import sqlite3
import os

# ── Database path ──
DB_DIR = os.path.join(os.path.dirname(__file__), "data", "database")
GRAPH_DIR = os.path.join(os.path.dirname(__file__), "data", "graph")
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "changsha_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, "changsha_network.gexf")

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA (hard-coded)
# ═══════════════════════════════════════════════════════════

persons = [
    # ── 陈竞 - 长沙市委书记 (Party Secretary) ──
    {"id": 1, "name": "陈竞", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-02", "birthplace": "湖南长沙", "education": "在职大学（中共湖南省委党校）",
     "party_join": "1993-12", "work_start": "1990-07",
     "current_post": "湖南省副省长、长沙市委书记", "current_org": "中共长沙市委",
     "source": "https://zh.wikipedia.org/wiki/%E9%99%88%E7%AB%9E_(1971%E5%B9%B4)"},

    # ── 陈博彰 - 长沙市市长 (Mayor) ──
    {"id": 2, "name": "陈博彰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市人民政府市长", "current_org": "长沙市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E9%95%BF%E6%B2%99%E5%B8%82%E5%B8%82%E9%95%BF%E5%88%97%E8%A1%A8"},

    # ── 周健 - 市委副书记（湘江新区书记）──
    {"id": 3, "name": "周健", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-11", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市委副书记、湘江新区党工委书记、岳麓区委书记",
     "current_org": "中共长沙市委",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E9%95%BF%E6%B2%99%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 吴桂英 - 前任长沙市委书记 ──
    {"id": 4, "name": "吴桂英", "gender": "女", "ethnicity": "汉族",
     "birth": "1966-02", "birthplace": "河北唐山", "education": "中国政法大学经济法系，研究生学历，哲学博士",
     "party_join": "1987-04", "work_start": "1990-02",
     "current_post": "湖南省人大常委会党组书记、副主任",
     "current_org": "湖南省人大常委会",
     "source": "https://zh.wikipedia.org/wiki/%E5%90%B4%E6%A1%82%E8%8B%B1_(1966%E5%B9%B4)"},

    # ── 李铁华 - 组织部部长 ──
    {"id": 5, "name": "李铁华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市委组织部部长", "current_org": "中共长沙市委",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E9%95%BF%E6%B2%99%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 张敏 - 政法委书记 ──
    {"id": 6, "name": "张敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市委政法委书记", "current_org": "中共长沙市委",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E9%95%BF%E6%B2%99%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 伍贤运 - 宣传部部长 ──
    {"id": 7, "name": "伍贤运", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市委宣传部部长", "current_org": "中共长沙市委",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E9%95%BF%E6%B2%99%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 周敏 - 湖南自贸区长沙片区书记 ──
    {"id": 8, "name": "周敏", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市委常委、湖南自贸区长沙片区党工委书记",
     "current_org": "中共长沙市委",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E9%95%BF%E6%B2%99%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 陈刚 - 市纪委书记 ──
    {"id": 9, "name": "陈刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市委常委、市纪委书记、市监委主任",
     "current_org": "中共长沙市纪律检查委员会",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E9%95%BF%E6%B2%99%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 周凡 - 市委秘书长 ──
    {"id": 10, "name": "周凡", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市委常委、市委秘书长",
     "current_org": "中共长沙市委",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E9%95%BF%E6%B2%99%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 易长运 - 长沙警备区政委 ──
    {"id": 11, "name": "易长运", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市委常委、长沙警备区政委",
     "current_org": "长沙警备区",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E9%95%BF%E6%B2%99%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 付旭明 - 常务副市长 ──
    {"id": 12, "name": "付旭明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市委常委、常务副市长",
     "current_org": "长沙市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E9%95%BF%E6%B2%99%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 胡小刚 - 浏阳市委书记 ──
    {"id": 13, "name": "胡小刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市委常委、浏阳市委书记",
     "current_org": "中共浏阳市委",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E9%95%BF%E6%B2%99%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 周春晖 - 统战部部长 ──
    {"id": 14, "name": "周春晖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "长沙市委常委、统战部部长",
     "current_org": "中共长沙市委",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E9%95%BF%E6%B2%99%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 郑建新 - 前市长（2020-2023）──
    {"id": 15, "name": "郑建新", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原长沙市长，2023年5月离任）",
     "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E9%95%BF%E6%B2%99%E5%B8%82%E5%B8%82%E9%95%BF%E5%88%97%E8%A1%A8"},

    # ── 周海兵 - 前市长（2023-2025）──
    {"id": 16, "name": "周海兵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原长沙市长，2025年5月离任）",
     "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E9%95%BF%E6%B2%99%E5%B8%82%E5%B8%82%E9%95%BF%E5%88%97%E8%A1%A8"},

    # ── 胡衡华 - 前书记（2017-2020）──
    {"id": 17, "name": "胡衡华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原长沙市委书记，2017-2020）",
     "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E8%83%A1%E8%A1%A1%E5%8D%8E"},
]

organizations = [
    {"id": 1, "name": "中共长沙市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "长沙"},
    {"id": 2, "name": "长沙市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "长沙"},
    {"id": 3, "name": "中共长沙市纪律检查委员会", "type": "党委", "level": "地市级", "parent": "中共长沙市委", "location": "长沙"},
    {"id": 4, "name": "长沙警备区", "type": "军队", "level": "地市级", "parent": "", "location": "长沙"},
    {"id": 5, "name": "湖南湘江新区", "type": "政府", "level": "地市级", "parent": "长沙市人民政府", "location": "长沙"},
    {"id": 6, "name": "湖南自贸区长沙片区", "type": "政府", "level": "地市级", "parent": "长沙市人民政府", "location": "长沙"},
    {"id": 7, "name": "中共浏阳市委", "type": "党委", "level": "县级", "parent": "中共长沙市委", "location": "浏阳"},
    {"id": 8, "name": "湖南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "长沙"},
    {"id": 9, "name": "中共湖南省委", "type": "党委", "level": "省级", "parent": "", "location": "长沙"},
    {"id": 10, "name": "湖南省人大常委会", "type": "政府", "level": "省级", "parent": "", "location": "长沙"},
    {"id": 11, "name": "中共益阳市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "益阳"},
    {"id": 12, "name": "益阳市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "益阳"},
    {"id": 13, "name": "中共湖南省委组织部", "type": "党委", "level": "省级", "parent": "中共湖南省委", "location": "长沙"},
    {"id": 14, "name": "中国建设银行", "type": "企业", "level": "企业", "parent": "", "location": "北京"},
    {"id": 15, "name": "共青团湖南省委", "type": "群众团体", "level": "省级", "parent": "", "location": "长沙"},
    {"id": 16, "name": "中共张家界市永定区委", "type": "党委", "level": "县级", "parent": "", "location": "张家界"},
    {"id": 17, "name": "中共慈利县委", "type": "党委", "level": "县级", "parent": "", "location": "慈利"},
    {"id": 18, "name": "中共衡阳市石鼓区委", "type": "党委", "level": "县级", "parent": "", "location": "衡阳"},
    {"id": 19, "name": "衡阳市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "衡阳"},
    {"id": 20, "name": "中共衡阳市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "衡阳"},
    {"id": 21, "name": "湖南省公务员局", "type": "政府", "level": "省级", "parent": "湖南省人民政府", "location": "长沙"},
    {"id": 22, "name": "北京市朝阳区人民政府", "type": "政府", "level": "地市级", "parent": "", "location": "北京"},
    {"id": 23, "name": "中共北京市朝阳区委", "type": "党委", "level": "地市级", "parent": "", "location": "北京"},
    {"id": 24, "name": "北京市工商局", "type": "政府", "level": "地市级", "parent": "", "location": "北京"},
    {"id": 25, "name": "北京市发改委", "type": "政府", "level": "地市级", "parent": "", "location": "北京"},
    {"id": 26, "name": "长沙市节约用水办公室", "type": "事业单位", "level": "县级", "parent": "长沙市人民政府", "location": "长沙"},
]

# Positions: person_id, org_id, title, start, end, rank, note
positions = [
    # ── 陈竞 (id=1) ──
    {"person_id": 1, "org_id": 1, "title": "长沙市委书记", "start": "2026-06", "end": "", "rank": "副部级", "note": "省委常委"},
    {"person_id": 1, "org_id": 8, "title": "湖南省副省长", "start": "2025-07", "end": "", "rank": "副部级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "益阳市委书记", "start": "2023-02", "end": "2026-05", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "益阳市人民政府市长", "start": "2021-08", "end": "2023-02", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "湖南省委组织部副部长、省公务员局局长", "start": "2019-10", "end": "2021-07", "rank": "正厅级", "note": "2019任部务委员，2021.04任副部长"},
    {"person_id": 1, "org_id": 21, "title": "湖南省公务员局局长", "start": "2019-10", "end": "2021-08", "rank": "正厅级", "note": "兼任"},
    {"person_id": 1, "org_id": 20, "title": "衡阳市委常委、组织部部长", "start": "2016-09", "end": "2019-10", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 19, "title": "衡阳市人民政府副市长", "start": "2015-02", "end": "2016-09", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 18, "title": "衡阳市石鼓区委书记", "start": "2013-12", "end": "2015-02", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "慈利县委书记", "start": "2011-12", "end": "2013-12", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 16, "title": "张家界市永定区委副书记、区长", "start": "2007-02", "end": "2011-12", "rank": "正处级", "note": "2007.02任代区长，2007.12正式任区长"},
    {"person_id": 1, "org_id": 15, "title": "共青团湖南省委青工部部长", "start": "2003-07", "end": "2007-02", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "共青团湖南省委青工部副部长", "start": "2000", "end": "2003-07", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "共青团湖南省委办公室副主任、组织部科长等", "start": "1995-04", "end": "2000", "rank": "科级", "note": "先后任青工部科员、副主任科员、企业科副科长、机关事业科科长、组织部组织科科长、办公室副主任等"},
    {"person_id": 1, "org_id": 14, "title": "中国建设银行长沙市分行职员", "start": "1994-12", "end": "1995-03", "rank": "企业", "note": "短暂在银行工作"},
    {"person_id": 1, "org_id": 26, "title": "长沙市节约用水办公室干部", "start": "1990-07", "end": "1994-12", "rank": "科员", "note": "第一份工作"},

    # ── 陈博彰 (id=2) ──
    {"person_id": 2, "org_id": 2, "title": "长沙市人民政府市长", "start": "2025-11", "end": "", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "长沙市委副书记", "start": "2025-11", "end": "", "rank": "正厅级", "note": ""},

    # ── 周健 (id=3) ──
    {"person_id": 3, "org_id": 1, "title": "长沙市委副书记", "start": "2025-11", "end": "", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 5, "title": "湘江新区党工委书记", "start": "2025-11", "end": "", "rank": "正厅级", "note": "兼长沙高新区党工委书记"},

    # ── 吴桂英 (id=4) ──
    {"person_id": 4, "org_id": 10, "title": "湖南省人大常委会党组书记、副主任", "start": "2026-02", "end": "", "rank": "副部级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "长沙市委书记", "start": "2021-02", "end": "2026-06", "rank": "副部级", "note": "省委常委"},
    {"person_id": 4, "org_id": 8, "title": "湖南省副省长", "start": "2018-01", "end": "2021-02", "rank": "副部级", "note": ""},
    {"person_id": 4, "org_id": 23, "title": "北京市朝阳区委书记", "start": "2015-09", "end": "2018-01", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 22, "title": "北京市朝阳区区长", "start": "2012-07", "end": "2015-11", "rank": "正厅级", "note": "2012.07代区长，2012.11正式当选"},
    {"person_id": 4, "org_id": 22, "title": "北京市朝阳区委常委、副区长", "start": "2008-05", "end": "2012-07", "rank": "副厅级", "note": "兼北京商务中心区管委会主任"},
    {"person_id": 4, "org_id": 25, "title": "北京市发改委副主任", "start": "2001-11", "end": "2008-05", "rank": "副厅级", "note": "原北京市计委"},
    {"person_id": 4, "org_id": 24, "title": "北京市工商局法制处处长", "start": "1997", "end": "2001-11", "rank": "正处级", "note": "先后任法制处科员、副主任科员、主任科员、副处长、处长、机场分局局长"},
    {"person_id": 4, "org_id": 24, "title": "北京市工商局干部", "start": "1991-04", "end": "1997", "rank": "科员", "note": ""},

    # ── 李铁华、张敏、伍贤运等 position in 长沙市委 ──
    {"person_id": 5, "org_id": 1, "title": "长沙市委组织部部长", "start": "2025-02", "end": "", "rank": "副厅级", "note": "市委常委"},
    {"person_id": 6, "org_id": 1, "title": "长沙市委政法委书记", "start": "", "end": "", "rank": "副厅级", "note": "市委常委"},
    {"person_id": 7, "org_id": 1, "title": "长沙市委宣传部部长", "start": "", "end": "", "rank": "副厅级", "note": "市委常委"},
    {"person_id": 8, "org_id": 1, "title": "长沙市委常委", "start": "2024-10", "end": "", "rank": "副厅级", "note": "湖南自贸区长沙片区党工委书记"},
    {"person_id": 8, "org_id": 6, "title": "湖南自贸区长沙片区党工委书记", "start": "", "end": "", "rank": "正厅级", "note": "兼任"},
    {"person_id": 9, "org_id": 1, "title": "长沙市委常委、市纪委书记", "start": "2023-05", "end": "", "rank": "副厅级", "note": "市监委主任"},
    {"person_id": 9, "org_id": 3, "title": "长沙市纪委书记、市监委主任", "start": "2023-05", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "长沙市委常委、市委秘书长", "start": "2025-12", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "长沙市委常委", "start": "", "end": "", "rank": "副厅级", "note": "长沙警备区政委"},
    {"person_id": 11, "org_id": 4, "title": "长沙警备区政委", "start": "", "end": "", "rank": "正师级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "长沙市委常委、常务副市长", "start": "2025-12", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "长沙市委常委", "start": "2026-05", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 7, "title": "浏阳市委书记", "start": "", "end": "", "rank": "正处级", "note": "兼任"},
    {"person_id": 14, "org_id": 1, "title": "长沙市委常委、统战部部长", "start": "2026-06", "end": "", "rank": "副厅级", "note": ""},
]

relationships = [
    # ── 党政正副搭班 ──
    {"person_a": 1, "person_b": 2, "type": "work_together",
     "context": "2026年6月起陈竞（市委书记）与陈博彰（市长）搭班任职长沙市委",
     "overlap_org": "中共长沙市委", "overlap_period": "2026-06至今"},

    # ── 前后任书记 ──
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor",
     "context": "陈竞2026年6月接替吴桂英任长沙市委书记",
     "overlap_org": "中共长沙市委", "overlap_period": "2026-06"},

    # ── 湖南省委-长沙市委上下级 ──
    {"person_a": 1, "person_b": 5, "type": "work_together",
     "context": "陈竞（书记）与李铁华（组织部长）在长沙市委共事",
     "overlap_org": "中共长沙市委", "overlap_period": "2026-06至今"},

    {"person_a": 1, "person_b": 6, "type": "work_together",
     "context": "长沙市委常委班子",
     "overlap_org": "中共长沙市委", "overlap_period": "2026-06至今"},

    {"person_a": 1, "person_b": 9, "type": "work_together",
     "context": "陈竞（书记）与陈刚（纪委书记）在长沙市委共事",
     "overlap_org": "中共长沙市委", "overlap_period": "2026-06至今"},

    # ── 湖南省级关系 ──
    {"person_a": 4, "person_b": 1, "type": "politics",
     "context": "吴桂英（省人大常委会）与陈竞（副省长/长沙书记）同在湖南省领导层",
     "overlap_org": "湖南省", "overlap_period": "2025-07至今"},
]

# ═══════════════════════════════════════════════════════════
# BUILD SQLite DATABASE
# ═══════════════════════════════════════════════════════════

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
DROP TABLE IF EXISTS relationships;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS organizations;
DROP TABLE IF EXISTS persons;

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
);

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

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
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

# Insert persons
for p in persons:
    c.execute("""
        INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

# Insert organizations
for o in organizations:
    c.execute("""
        INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

# Insert positions
for pos in positions:
    c.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

# Insert relationships
for r in relationships:
    c.execute("""
        INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))

conn.commit()

# Summary
person_count = c.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
org_count = c.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
pos_count = c.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
rel_count = c.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]

print(f"✅ SQLite DB: {DB_PATH}")
print(f"   Persons: {person_count}")
print(f"   Organizations: {org_count}")
print(f"   Positions: {pos_count}")
print(f"   Relationships: {rel_count}")

conn.close()


# ═══════════════════════════════════════════════════════════
# BUILD GEXF GRAPH
# ═══════════════════════════════════════════════════════════

# Color mapping for nodes
def node_color(person):
    name = person["name"]
    if name == "陈竞":
        return "#E03C31", "Party Secretary"
    elif name in ["吴桂英", "胡衡华"]:
        return "#E03C31", "Former Party Secretary"
    elif "市长" in person.get("current_post", "") or "区长" in person.get("current_post", ""):
        return "#3B82F6", "Government"
    elif "纪委书记" in person.get("current_post", ""):
        return "#F59E0B", "Discipline"
    elif "政委" in person.get("current_post", ""):
        return "#8B5CF6", "Military"
    else:
        return "#6B7280", "Other"


def escape_xml(s):
    if s is None:
        return ""
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;"))


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append('  <graph defaultedgetype="undirected">')

lines.append('    <attributes class="node">')
lines.append('      <attribute id="role" title="Role" type="string"/>')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="edge_type" title="Edge Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

lines.append('    <nodes>')
for p in persons:
    pcolor, prole = node_color(p)
    size = "20.0" if p["name"] in ["陈竞", "吴桂英"] else "12.0"
    lines.append(f'      <node id="person_{p["id"]}" label="{escape_xml(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="role" value="{escape_xml(prole)}"/>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{escape_xml(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{escape_xml(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{escape_xml(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{escape_xml(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{escape_xml(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(pcolor[1:3], 16)}" g="{int(pcolor[3:5], 16)}" b="{int(pcolor[5:7], 16)}" a="1.0"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'        <viz:shape value="disc"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

edge_id = 0
lines.append('    <edges>')
for pos in positions:
    pid = pos["person_id"]
    oid = pos["org_id"]
    edge_id += 1
    context = f"{pos['title']} ({pos.get('start','')}-{pos.get('end','')})"
    lines.append(f'      <edge id="e{edge_id}" source="person_{pid}" target="org_{oid}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="edge_type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{escape_xml(context)}"/>')
    lines.append(f'          <attvalue for="period" value="{escape_xml(pos.get("start",""))}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')

for r in relationships:
    edge_id += 1
    lines.append(f'      <edge id="e{edge_id}" source="person_{r["person_a"]}" target="person_{r["person_b"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="edge_type" value="relationship"/>')
    lines.append(f'          <attvalue for="context" value="{escape_xml(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{escape_xml(r.get("overlap_period",""))}"/>')
    lines.append(f'        </attvalues>')
    if r["type"] == "work_together":
        lines.append(f'        <viz:color r="201" g="169" b="78" a="1.0"/>')
        lines.append(f'        <viz:thickness value="3.0"/>')
    else:
        lines.append(f'        <viz:color r="96" g="165" b="250" a="1.0"/>')
        lines.append(f'        <viz:thickness value="1.5"/>')
    lines.append(f'      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF: {GEXF_PATH}")
print(f"   Edges: {edge_id}")
print("✅ Done!")
