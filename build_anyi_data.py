#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Anyi County leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/anyi_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/anyi_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current and Recent Anyi County Party Secretaries ──
    {"id": 1, "name": "熊辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-03", "birthplace": "江西奉新", "education": "博士研究生",
     "party_join": "2006-05", "work_start": "2002-09",
     "current_post": "中共安义县委书记", "current_org": "中共安义县委员会",
     "source": "https://www.163.com/dy/article/L1LE2GI505563DJA.html"},
    {"id": 2, "name": "谭伯乐", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-08", "birthplace": "江西进贤", "education": "中央党校大学",
     "party_join": "1991-10", "work_start": "1990-08",
     "current_post": "南昌市政协副主席", "current_org": "南昌市政协",
     "source": "https://jx.sina.com.cn/news/b/2025-01-13/detail-ineeutxf9760625.shtml"},
    {"id": 3, "name": "彭开先", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-02", "birthplace": "江西余干", "education": "在职大专/哲学硕士",
     "party_join": "1994-09", "work_start": "1988-07",
     "current_post": "南昌市人民政府副市长", "current_org": "南昌市人民政府",
     "source": "https://www.nc.gov.cn/ncszf/pengkx/2021_ldzc.shtml"},
    {"id": 4, "name": "乐文红", "gender": "女", "ethnicity": "汉族",
     "birth": "1970-02", "birthplace": "江西贵溪", "education": "中央党校研究生",
     "party_join": "1996-09", "work_start": "1989-08",
     "current_post": "江西省委统战部一级巡视员", "current_org": "江西省委统战部",
     "source": "https://jiangxi.jxnews.com.cn/system/2024/01/29/020387023.shtml"},
    {"id": 5, "name": "李松殿", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-11", "birthplace": "江西南昌(新建)", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1988-08",
     "current_post": "南昌市人民政府副市长", "current_org": "南昌市人民政府",
     "source": "http://renshi.people.com.cn/n1/2019/0430/c139617-31060115.html"},
    {"id": 6, "name": "邱向军", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-02", "birthplace": "江西资溪", "education": "江西师范大学法学博士/MBA",
     "party_join": "1988-01", "work_start": "1990-07",
     "current_post": "江西省民政厅党组书记、厅长", "current_org": "江西省民政厅",
     "source": "https://baike.baidu.com/item/%E9%82%B1%E5%90%91%E5%86%9B/13852998"},

    # ── Current Anyi County Government Leaders ──
    {"id": 7, "name": "罗国栋", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-10", "birthplace": "江西吉水", "education": "中央党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共青云谱区委书记", "current_org": "中共青云谱区委员会",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202108/866e2e6fc98d4a1ebb6d98c5cd3d2e50.shtml"},
    {"id": 8, "name": "杨峻", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-06", "birthplace": "江西南昌", "education": "研究生",
     "party_join": "2000-12", "work_start": "1996-09",
     "current_post": "安义县委常委、宣传部部长", "current_org": "中共安义县委员会",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202101/d0954437573a49b28a9ae7fe537c7ab9.shtml"},
    {"id": 9, "name": "刘志伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安义县委常委、常务副县长", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/ldzc/ldzc.shtml"},
    {"id": 10, "name": "詹晓庆", "gender": "女", "ethnicity": "汉族",
     "birth": "1981-12", "birthplace": "江西丰城", "education": "研究生",
     "party_join": "2004-11", "work_start": "2006-06",
     "current_post": "安义县委常委、组织部部长", "current_org": "中共安义县委员会",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202603/e13250fcb2604e6ea392f1fe04c01804.shtml"},
    {"id": 11, "name": "余建国", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-09", "birthplace": "江西安义", "education": "大学",
     "party_join": "1993-11", "work_start": "1992-08",
     "current_post": "安义县委常委、政法委书记", "current_org": "中共安义县委员会",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202009/a50250bfb6ca42b69c5b3ac2df6c98c0.shtml"},
    {"id": 12, "name": "张帆", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-09", "birthplace": "江西南昌", "education": "全日制大学/MPA",
     "party_join": "2007-09", "work_start": "2003-07",
     "current_post": "安义县委常委、统战部部长", "current_org": "中共安义县委员会",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202108/217fbf6d5eeb4c6386888ddbf4e9d403.shtml"},
    {"id": 13, "name": "谭翼直", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-05", "birthplace": "江西都昌", "education": "在职研究生/工商管理硕士",
     "party_join": "2007-12", "work_start": "2010-08",
     "current_post": "安义县委常委、常务副县长", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202307/17d36c36095f485ea22916e78ee99042.shtml"},
    {"id": 14, "name": "余超", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-08", "birthplace": "江西都昌", "education": "硕士研究生",
     "party_join": "2004-05", "work_start": "2008-06",
     "current_post": "安义县委常委、副县长", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202504/db551054acbd43cea5283a58933dc8a7.shtml"},
    {"id": 15, "name": "金栋", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-11", "birthplace": "江西乐平", "education": "在职研究生/法学硕士",
     "party_join": "2002-05", "work_start": "2002-07",
     "current_post": "安义县委常委、纪委书记、县监委主任", "current_org": "中共安义县纪律检查委员会",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202503/b17616c626134c6bb7b5984322628920.shtml"},
    {"id": 16, "name": "吴威", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-04", "birthplace": "河南遂平", "education": "大学",
     "party_join": "2008-07", "work_start": "2002-09",
     "current_post": "安义县委常委、人武部部长", "current_org": "安义县人民武装部",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202512/61884f6c5c2c49b89a208051029042df.shtml"},

    # ── Current Anyi County Deputy Mayors ──
    {"id": 17, "name": "万菁", "gender": "女", "ethnicity": "汉族",
     "birth": "1982-10", "birthplace": "江西南昌", "education": "大学本科",
     "party_join": "民盟盟员", "work_start": "2003-11",
     "current_post": "安义县副县长", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/govld/202503/6eb3b7908fb24f23a3e67d34eaf6a78e.shtml"},
    {"id": 18, "name": "刘彬", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安义县副县长、党组成员", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/govld/202108/5de6e026465e4fc3aa4ba242db4216cc.shtml"},
    {"id": 19, "name": "赵伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-02", "birthplace": "山东郓城", "education": "大学本科",
     "party_join": "2003-12", "work_start": "2004-07",
     "current_post": "安义县副县长、党组成员兼高新园区党工委书记", "current_org": "安义县人民政府",
     "source": "https://baike.baidu.com/item/%E8%B5%B5%E4%BC%9F/58349955"},
    {"id": 20, "name": "杨武", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-11", "birthplace": "江西进贤", "education": "博士研究生/理学博士",
     "party_join": "2017-11", "work_start": "2013-09",
     "current_post": "安义县副县长、党组成员", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/govld/202406/6af8f784cc5f4795832e47eacaa7a7f7.shtml"},
    {"id": 21, "name": "邓梁", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-05", "birthplace": "江西南昌", "education": "在职大学",
     "party_join": "2001-08", "work_start": "1995-08",
     "current_post": "安义县副县长、党组成员、县公安局局长", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/govld/202507/4f9f341fe4f14f6d87a10f369605fa84.shtml"},

    # ── Cross-County Network Figures ──
    {"id": 22, "name": "熊振强", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-03", "birthplace": "江西奉新", "education": "大学",
     "party_join": "1992-12", "work_start": "1991-09",
     "current_post": "中共进贤县委书记", "current_org": "中共进贤县委员会",
     "source": "https://www.163.com/dy/article/L1LE2GI505563DJA.html"},
    {"id": 23, "name": "袁一旦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "青山湖区委书记", "current_org": "中共青山湖区委员会",
     "source": "https://m.thepaper.cn/newsDetail_forward_1500196"},
    {"id": 24, "name": "杨志文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "江西安义", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "进贤县委常委、常务副县长", "current_org": "进贤县人民政府",
     "source": "https://m.thepaper.cn/newsDetail_forward_1500196"},
    {"id": 25, "name": "朱东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://zh.wikipedia.org/zh-cn/%E5%AE%89%E4%B9%89%E5%8E%BF"},
    {"id": 26, "name": "黄俊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://web.archive.org/web/20090423035327/http:/www.anyi.gov.cn/"},
]

organizations = [
    {"id": 1, "name": "中共安义县委员会", "type": "党委", "level": "县处级", "parent": "中共南昌市委员会", "location": "江西南昌安义"},
    {"id": 2, "name": "安义县人民政府", "type": "政府", "level": "县处级", "parent": "南昌市人民政府", "location": "江西南昌安义"},
    {"id": 3, "name": "中共安义县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共南昌市纪律检查委员会", "location": "江西南昌安义"},
    {"id": 4, "name": "安义县人民武装部", "type": "军事", "level": "县处级", "parent": "", "location": "江西南昌安义"},
    {"id": 5, "name": "南昌市政协", "type": "政协", "level": "副厅级", "parent": "", "location": "江西南昌"},
    {"id": 6, "name": "南昌市人民政府", "type": "政府", "level": "副省级", "parent": "江西省人民政府", "location": "江西南昌"},
    {"id": 7, "name": "江西省委统战部", "type": "党委部门", "level": "厅级", "parent": "中共江西省委", "location": "江西南昌"},
    {"id": 8, "name": "江西省民政厅", "type": "政府", "level": "厅级", "parent": "江西省人民政府", "location": "江西南昌"},
    {"id": 9, "name": "中共青云谱区委员会", "type": "党委", "level": "县处级", "parent": "中共南昌市委员会", "location": "江西南昌青云谱"},
    {"id": 10, "name": "中共进贤县委员会", "type": "党委", "level": "县处级", "parent": "中共南昌市委员会", "location": "江西南昌进贤"},
    {"id": 11, "name": "进贤县人民政府", "type": "政府", "level": "县处级", "parent": "南昌市人民政府", "location": "江西南昌进贤"},
]

positions = [
    # ── Xiong Hui (熊辉) career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共安义县委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 11, "title": "进贤县委副书记、县长", "start": "", "end": "2026-07", "rank": "县处级正职", "note": "前任职务"},
    {"id": 3, "person_id": 1, "org_id": 9, "title": "青云谱区委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "更早职务"},
    {"id": 4, "person_id": 1, "org_id": 9, "title": "青云谱区副区长", "start": "", "end": "", "rank": "县处级副职", "note": "更早职务"},

    # ── Tan Bole (谭伯乐) career ──
    {"id": 5, "person_id": 2, "org_id": 1, "title": "中共安义县委书记", "start": "2021-08", "end": "2026-07", "rank": "县处级正职", "note": ""},
    {"id": 6, "person_id": 2, "org_id": 5, "title": "南昌市政协副主席", "start": "2025-01", "end": "", "rank": "副厅级", "note": "兼任安义县委书记至2026年7月"},
    {"id": 7, "person_id": 2, "org_id": 2, "title": "安义县人民政府县长", "start": "2020-04", "end": "2021-08", "rank": "县处级正职", "note": ""},
    {"id": 8, "person_id": 2, "org_id": 10, "title": "南昌县委副书记", "start": "", "end": "2019-12", "rank": "县处级副职", "note": ""},

    # ── Peng Kaixian (彭开先) career ──
    {"id": 9, "person_id": 3, "org_id": 1, "title": "中共安义县委书记", "start": "2020-01", "end": "2021-08", "rank": "县处级正职", "note": ""},
    {"id": 10, "person_id": 3, "org_id": 6, "title": "南昌市人民政府副市长", "start": "2021", "end": "", "rank": "副厅级", "note": ""},
    {"id": 11, "person_id": 3, "org_id": 2, "title": "安义县人民政府县长", "start": "2016-10", "end": "2020-01", "rank": "县处级正职", "note": ""},
    {"id": 12, "person_id": 3, "org_id": 1, "title": "安义县委副书记", "start": "2015-07", "end": "2016-08", "rank": "县处级副职", "note": ""},

    # ── Yue Wenhong (乐文红) career ──
    {"id": 13, "person_id": 4, "org_id": 1, "title": "中共安义县委书记（兼任）", "start": "2019-09", "end": "2020-01", "rank": "县处级正职", "note": "以南昌市委常委、统战部长身份兼任"},
    {"id": 14, "person_id": 4, "org_id": 7, "title": "江西省委统战部一级巡视员", "start": "2024", "end": "", "rank": "厅级", "note": ""},

    # ── Li Songdian (李松殿) career ──
    {"id": 15, "person_id": 5, "org_id": 1, "title": "中共安义县委书记", "start": "2014-09", "end": "2019-03", "rank": "县处级正职", "note": ""},
    {"id": 16, "person_id": 5, "org_id": 6, "title": "南昌市人民政府副市长", "start": "2019-04", "end": "", "rank": "副厅级", "note": ""},

    # ── Qiu Xiangjun (邱向军) career ──
    {"id": 17, "person_id": 6, "org_id": 1, "title": "中共安义县委书记", "start": "2005-05", "end": "2008-12", "rank": "县处级正职", "note": ""},
    {"id": 18, "person_id": 6, "org_id": 8, "title": "江西省民政厅党组书记、厅长", "start": "2025-07", "end": "", "rank": "厅级", "note": "现任"},

    # ── Luo Guodong (罗国栋) career ──
    {"id": 19, "person_id": 7, "org_id": 9, "title": "中共青云谱区委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "新任"},
    {"id": 20, "person_id": 7, "org_id": 2, "title": "安义县人民政府县长", "start": "2021-08", "end": "2026-07", "rank": "县处级正职", "note": ""},

    # ── Yang Jun (杨峻) ──
    {"id": 21, "person_id": 8, "org_id": 1, "title": "安义县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Liu Zhiwei (刘志伟) ──
    {"id": 22, "person_id": 9, "org_id": 2, "title": "安义县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Zhan Xiaoqing (詹晓庆) ──
    {"id": 23, "person_id": 10, "org_id": 1, "title": "安义县委常委、组织部部长", "start": "2026", "end": "", "rank": "县处级副职", "note": "新任"},

    # ── Yu Jianguo (余建国) ──
    {"id": 24, "person_id": 11, "org_id": 1, "title": "安义县委常委、政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Zhang Fan (张帆) ──
    {"id": 25, "person_id": 12, "org_id": 1, "title": "安义县委常委、统战部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Tan Yizhi (谭翼直) ──
    {"id": 26, "person_id": 13, "org_id": 2, "title": "安义县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Yu Chao (余超) ──
    {"id": 27, "person_id": 14, "org_id": 2, "title": "安义县委常委、副县长", "start": "2025", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Jin Dong (金栋) ──
    {"id": 28, "person_id": 15, "org_id": 3, "title": "安义县委常委、纪委书记、县监委主任", "start": "2025", "end": "", "rank": "县处级副职", "note": "新任"},

    # ── Wu Wei (吴威) ──
    {"id": 29, "person_id": 16, "org_id": 4, "title": "安义县委常委、人武部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Deputy Mayors ──
    {"id": 30, "person_id": 17, "org_id": 2, "title": "安义县副县长", "start": "2025-02", "end": "", "rank": "县处级副职", "note": "现任, 民盟"},
    {"id": 31, "person_id": 18, "org_id": 2, "title": "安义县副县长、党组成员", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 32, "person_id": 19, "org_id": 2, "title": "安义县副县长、党组成员", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 33, "person_id": 20, "org_id": 2, "title": "安义县副县长、党组成员", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 34, "person_id": 21, "org_id": 2, "title": "安义县副县长、党组成员、县公安局局长", "start": "2025", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Cross-county figures ──
    {"id": 35, "person_id": 22, "org_id": 10, "title": "中共进贤县委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "新任，曾任安义县委常委"},
    {"id": 36, "person_id": 23, "org_id": 6, "title": "青山湖区委书记", "start": "", "end": "", "rank": "县处级正职", "note": "曾任安义县副县长"},
    {"id": 37, "person_id": 24, "org_id": 10, "title": "进贤县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "安义籍，曾任安义镇党委书记"},
    {"id": 38, "person_id": 25, "org_id": 1, "title": "中共安义县委书记", "start": "2012", "end": "2014-09", "rank": "县处级正职", "note": ""},
    {"id": 39, "person_id": 26, "org_id": 1, "title": "中共安义县委书记", "start": "2009", "end": "2012", "rank": "县处级正职", "note": ""},
]

relationships = [
    # ── Predecessor-Successor ──
    {"id": 1, "person_a_id": 2, "person_b_id": 1, "type": "交接", "context": "谭伯乐→熊辉 安义县委书记交接（2026年7月）", "overlap_org": "中共安义县委员会", "overlap_period": "2026-07"},
    {"id": 2, "person_a_id": 3, "person_b_id": 2, "type": "交接", "context": "彭开先→谭伯乐 安义县委书记交接（2021年8月）", "overlap_org": "中共安义县委员会", "overlap_period": "2021-08"},
    {"id": 3, "person_a_id": 4, "person_b_id": 3, "type": "交接", "context": "乐文红→彭开先 安义县委书记交接（2020年1月）", "overlap_org": "中共安义县委员会", "overlap_period": "2020-01"},
    {"id": 4, "person_a_id": 5, "person_b_id": 4, "type": "交接", "context": "李松殿→乐文红 安义县委书记交接（2019年9月）", "overlap_org": "中共安义县委员会", "overlap_period": "2019-09"},

    # ── Cross-County Connections ──
    {"id": 5, "person_a_id": 1, "person_b_id": 22, "type": "跨县调动", "context": "熊辉、熊振强同期调动，熊振强曾任安义县委常委，熊辉任安义县委书记", "overlap_org": "", "overlap_period": "2026-07"},
    {"id": 6, "person_a_id": 7, "person_b_id": 1, "type": "党政搭档", "context": "罗国栋曾任安义县长，熊辉任安义县委书记，后罗国栋调任青云谱区委书记", "overlap_org": "安义县人民政府", "overlap_period": "2026-07"},
    {"id": 7, "person_a_id": 23, "person_b_id": 1, "type": "跨县调动", "context": "袁一旦曾任安义县副县长，后任青山湖区委书记", "overlap_org": "", "overlap_period": "2006-2011"},

    # ── Existing Coworkers in Anyi ──
    {"id": 8, "person_a_id": 8, "person_b_id": 9, "type": "同僚", "context": "杨峻与刘志伟均为安义县委常委", "overlap_org": "中共安义县委员会", "overlap_period": ""},
    {"id": 9, "person_a_id": 10, "person_b_id": 11, "type": "同僚", "context": "詹晓庆与余建国均为安义县委常委", "overlap_org": "中共安义县委员会", "overlap_period": ""},
    {"id": 10, "person_a_id": 12, "person_b_id": 13, "type": "同僚", "context": "张帆与谭翼直均为安义县委常委", "overlap_org": "中共安义县委员会", "overlap_period": ""},

    # ── County Mayor-Secretary connections ──
    {"id": 11, "person_a_id": 2, "person_b_id": 3, "type": "党政搭档", "context": "彭开先任县委书记时，谭伯乐任县长", "overlap_org": "安义县人民政府", "overlap_period": "2020-2021"},
    {"id": 12, "person_a_id": 3, "person_b_id": 5, "type": "党政搭档", "context": "李松殿任县委书记时，彭开先先后任常务副县长、副书记", "overlap_org": "中共安义县委员会", "overlap_period": "2014-2019"},

    # ── Anyi → Jinxian flow ──
    {"id": 13, "person_a_id": 23, "person_b_id": 24, "type": "跨县交流", "context": "袁一旦与杨志文均由安义调至进贤", "overlap_org": "", "overlap_period": ""},

    # ── Luo Guodong and Xiong Hui ──
    {"id": 14, "person_a_id": 7, "person_b_id": 2, "type": "党政搭档", "context": "谭伯乐任县委书记时，罗国栋任县长", "overlap_org": "安义县人民政府", "overlap_period": "2021-2026"},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
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
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>安义县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    if p["id"] in [1, 2, 22]:
        color = '#E03C31'  # red: Party Secretary
        size = 20.0
    elif p["id"] in [3, 7]:
        color = '#2980B9'  # blue: government leader
        size = 18.0
    elif p["id"] in [4]:
        color = '#E67E22'  # orange: concurrent/special
        size = 16.0
    elif p["id"] in [15]:
        color = '#E67E22'  # orange: discipline
        size = 16.0
    else:
        color = '#95A5A6'  # grey: others
        size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
