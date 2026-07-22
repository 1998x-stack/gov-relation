#!/usr/bin/env python3
"""
蕉岭县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
City: 梅州市
Region: 蕉岭县
Targets: 县委书记 & 县长

Research Date: 2026-07-22
Data Sources: jiaoling.gov.cn (official), baike.baidu.com, news articles
Web access: Exa rate-limited, Baidu 403 (partial via direct IP), Meizhou gov 521
"""

import os
import sqlite3
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
STAGING_DB = os.path.join(BASE, "蕉岭县_network.db")
STAGING_GEXF = os.path.join(BASE, "蕉岭县_network.gexf")

# Token declarations for process_tmp.py validation
DB_PATH = STAGING_DB
GEXF_PATH = STAGING_GEXF

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘鸿涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共蕉岭县委书记、蕉华工业园区党委书记",
        "current_org": "中共蕉岭县委员会",
        "source": "https://www.jiaoling.gov.cn/ — 多篇领导活动新闻确认县委书记身份。百度百科词条存在但无详细履历。https://baike.baidu.com/item/%E5%88%98%E9%B8%BF%E6%B6%9B/23189558"
    },
    {
        "id": 2,
        "name": "刘裕君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "广东丰顺",
        "education": "省委党校大学（仲恺农业技术学院大专+省委党校经济管理本科）",
        "party_join": "2001年1月",
        "work_start": "1995年8月",
        "current_post": "中共蕉岭县委副书记、县政府党组书记、县长，广东梅州蕉华工业园区党委副书记、管委会主任",
        "current_org": "蕉岭县人民政府",
        "source": "https://www.jiaoling.gov.cn/zwgk/ldzc/ (官方简历)。https://baike.baidu.com/item/%E5%88%98%E8%A3%95%E5%90%9B (详细履历)"
    },
    {
        "id": 3,
        "name": "胡班",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共蕉岭县委副书记、政法委书记",
        "current_org": "中共蕉岭县委员会",
        "source": "https://www.jiaoling.gov.cn/zwgk/ldhd/content/post_2715422.html — 2024年12月新闻确认"
    },
    {
        "id": 4,
        "name": "肖纯辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共蕉岭县委副书记（省纵向帮扶队长）",
        "current_org": "中共蕉岭县委员会",
        "source": "https://baike.baidu.com/item/%E8%82%96%E7%BA%AF%E8%BE%89 — 省市场监管局粤西稽查办副主任下派"
    },
    {
        "id": 5,
        "name": "徐永岭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "广东蕉岭",
        "education": "省委党校大学（省委党校经济管理专业）",
        "party_join": "1998年11月",
        "work_start": "1995年8月",
        "current_post": "中共蕉岭县委常委、县政府党组副书记、副县长（常务）",
        "current_org": "蕉岭县人民政府",
        "source": "https://baike.baidu.com/item/%E5%BE%90%E6%B0%B8%E5%B2%AD"
    },
    {
        "id": 6,
        "name": "王映萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共蕉岭县委常委、副县长",
        "current_org": "蕉岭县人民政府",
        "source": "https://www.jiaoling.gov.cn/zwgk/ldhd/content/post_2925005.html"
    },
    {
        "id": 7,
        "name": "黄鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共蕉岭县委常委、县纪委书记、县监委主任、蕉华工业园区纪委书记",
        "current_org": "中共蕉岭县纪律检查委员会",
        "source": "https://www.jiaoling.gov.cn/zwgk/ldhd/content/post_2676776.html"
    },
    {
        "id": 8,
        "name": "谢伟传",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共蕉岭县委常委、组织部部长",
        "current_org": "中共蕉岭县委员会",
        "source": "https://baike.baidu.com/item/%E8%B0%A2%E4%BC%9F%E4%BC%A0. 蕉岭县政府官网2025-2026年多篇领导活动新闻"
    },
    {
        "id": 9,
        "name": "陈丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共蕉岭县委常委、宣传部部长",
        "current_org": "中共蕉岭县委员会",
        "source": "蕉岭县政府官网领导活动页面"
    },
    {
        "id": 10,
        "name": "丘文慈",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年3月",
        "birthplace": "广东蕉岭",
        "education": "大学（中央广播电视大学行政管理专业）",
        "party_join": "1994年5月",
        "work_start": "1994年8月",
        "current_post": "中共蕉岭县委常委、县委办公室主任、统战部部长、党群系统党委书记",
        "current_org": "中共蕉岭县委员会",
        "source": "https://baike.baidu.com/item/%E4%B8%98%E6%96%87%E6%85%88"
    },
    {
        "id": 11,
        "name": "王晓峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县委常委、县人武部",
        "current_org": "蕉岭县人民武装部",
        "source": "蕉岭县政府官网新闻"
    },
    {
        "id": 12,
        "name": "钟剑平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县副县长、县公安局局长",
        "current_org": "蕉岭县人民政府",
        "source": "蕉岭县政府官网多篇新闻"
    },
    {
        "id": 13,
        "name": "钟光庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县副县长",
        "current_org": "蕉岭县人民政府",
        "source": "蕉岭县政府官网新闻"
    },
    {
        "id": 14,
        "name": "张慧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县副县长",
        "current_org": "蕉岭县人民政府",
        "source": "蕉岭县政府官网 — 2026年县人大会议任命"
    },
    {
        "id": 15,
        "name": "李杜强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县副县长",
        "current_org": "蕉岭县人民政府",
        "source": "蕉岭县政府官网新闻"
    },
    {
        "id": 16,
        "name": "周锐明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县副县长（番禺对口帮扶队长）",
        "current_org": "蕉岭县人民政府",
        "source": "蕉岭县政府官网领导活动"
    },
    # ════════════════════════════════════════
    # 县人大
    # ════════════════════════════════════════
    {
        "id": 17,
        "name": "张伟杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县人大常委会主任",
        "current_org": "蕉岭县人大常委会",
        "source": "蕉岭县政府官网 — 县人大常委会会议新闻"
    },
    {
        "id": 18,
        "name": "江运洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县人大常委会副主任",
        "current_org": "蕉岭县人大常委会",
        "source": "蕉岭县政府官网 — 县人大常委会会议新闻"
    },
    {
        "id": 19,
        "name": "饶森健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县人大常委会副主任",
        "current_org": "蕉岭县人大常委会",
        "source": "蕉岭县政府官网 — 县人大常委会会议新闻"
    },
    {
        "id": 20,
        "name": "陈苑娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县人大常委会副主任",
        "current_org": "蕉岭县人大常委会",
        "source": "蕉岭县政府官网 — 县人大常委会会议新闻"
    },
    {
        "id": 21,
        "name": "丘志铭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县人大常委会副主任、县总工会主席",
        "current_org": "蕉岭县人大常委会",
        "source": "蕉岭县政府官网 — 县人大常委会会议新闻"
    },
    # ════════════════════════════════════════
    # 县政协
    # ════════════════════════════════════════
    {
        "id": 22,
        "name": "钟梅芬",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县政协主席",
        "current_org": "中国人民政治协商会议蕉岭县委员会",
        "source": "蕉岭县政府官网多篇新闻"
    },
    # ════════════════════════════════════════
    # 法检两院 & 其他
    # ════════════════════════════════════════
    {
        "id": 23,
        "name": "幸庆迈",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县人民法院院长",
        "current_org": "蕉岭县人民法院",
        "source": "蕉岭县政府官网 — 县人大常委会会议新闻"
    },
    {
        "id": 24,
        "name": "温建文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县人民检察院检察长",
        "current_org": "蕉岭县人民检察院",
        "source": "蕉岭县政府官网 — 县人大常委会会议新闻"
    },
    {
        "id": 25,
        "name": "李浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "蕉岭县纪委副书记、县监察委副主任",
        "current_org": "中共蕉岭县纪律检查委员会",
        "source": "蕉岭县政府官网 — 县人大常委会会议新闻"
    },
]

organizations = [
    {"id": 1, "name": "中共蕉岭县委员会", "type": "党委", "level": "县处级", "parent": "中共梅州市委员会", "location": "广东梅州蕉岭"},
    {"id": 2, "name": "蕉岭县人民政府", "type": "政府", "level": "县处级", "parent": "梅州市人民政府", "location": "广东梅州蕉岭"},
    {"id": 3, "name": "中共蕉岭县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共梅州市纪律检查委员会", "location": "广东梅州蕉岭"},
    {"id": 4, "name": "蕉岭县人大常委会", "type": "人大", "level": "县处级", "parent": "梅州市人大常委会", "location": "广东梅州蕉岭"},
    {"id": 5, "name": "蕉岭县政协", "type": "政协", "level": "县处级", "parent": "政协梅州市委员会", "location": "广东梅州蕉岭"},
    {"id": 6, "name": "蕉岭县人民法院", "type": "审判机关", "level": "县处级", "parent": "梅州市中级人民法院", "location": "广东梅州蕉岭"},
    {"id": 7, "name": "蕉岭县人民检察院", "type": "检察机关", "level": "县处级", "parent": "梅州市人民检察院", "location": "广东梅州蕉岭"},
    {"id": 8, "name": "蕉岭县人民武装部", "type": "军事", "level": "县处级", "parent": "", "location": "广东梅州蕉岭"},
    {"id": 9, "name": "广东梅州蕉华工业园区管理委员会", "type": "开发区", "level": "县处级", "parent": "梅州市人民政府", "location": "广东梅州蕉岭"},
    {"id": 10, "name": "蕉岭县总工会", "type": "群团", "level": "县处级", "parent": "", "location": "广东梅州蕉岭"},
    {"id": 11, "name": "大埔县人民政府", "type": "政府", "level": "县处级", "parent": "梅州市人民政府", "location": "广东梅州大埔"},
    {"id": 12, "name": "丰顺县农业委员会", "type": "政府", "level": "乡科级", "parent": "丰顺县人民政府", "location": "广东梅州丰顺"},
    {"id": 13, "name": "梅州市人民政府研究室", "type": "政府", "level": "处级", "parent": "梅州市人民政府", "location": "广东梅州"},
    {"id": 14, "name": "中共梅州市委办公室", "type": "党委部门", "level": "处级", "parent": "中共梅州市委员会", "location": "广东梅州"},
    {"id": 15, "name": "蕉岭县徐溪镇人民政府", "type": "乡镇/街道", "level": "乡科级", "parent": "蕉岭县人民政府", "location": "广东梅州蕉岭徐溪"},
    {"id": 16, "name": "蕉岭县蓝坊镇人民政府", "type": "乡镇/街道", "level": "乡科级", "parent": "蕉岭县人民政府", "location": "广东梅州蕉岭蓝坊"},
    {"id": 17, "name": "蕉岭县文福镇人民政府", "type": "乡镇/街道", "level": "乡科级", "parent": "蕉岭县人民政府", "location": "广东梅州蕉岭文福"},
    {"id": 18, "name": "蕉岭县科工商务管理局", "type": "政府", "level": "乡科级", "parent": "蕉岭县人民政府", "location": "广东梅州蕉岭"},
    {"id": 19, "name": "蕉岭县广福镇人民政府", "type": "乡镇/街道", "level": "乡科级", "parent": "蕉岭县人民政府", "location": "广东梅州蕉岭广福"},
    {"id": 20, "name": "蕉岭县人民政府办公室", "type": "政府", "level": "乡科级", "parent": "蕉岭县人民政府", "location": "广东梅州蕉岭"},
    {"id": 21, "name": "蕉岭县林业局", "type": "政府", "level": "乡科级", "parent": "蕉岭县人民政府", "location": "广东梅州蕉岭"},
    {"id": 22, "name": "蕉岭县长潭镇人民政府", "type": "乡镇/街道", "level": "乡科级", "parent": "蕉岭县人民政府", "location": "广东梅州蕉岭长潭"},
    {"id": 23, "name": "蕉岭县北礤镇人民政府", "type": "乡镇/街道", "level": "乡科级", "parent": "蕉岭县人民政府", "location": "广东梅州蕉岭北礤"},
]

positions = [
    # ── 刘鸿涛 (县委书记) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "蕉岭县委书记、蕉华工业园区党委书记", "start": "待查", "end": "今", "rank": "县处级正职", "note": "现任"},
    # ── 刘裕君 (县长) ──
    {"id": 2, "person_id": 2, "org_id": 2, "title": "蕉岭县委副书记、县长、蕉华工业园区管委会主任", "start": "2021?", "end": "今", "rank": "县处级正职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 11, "title": "大埔县委副书记、政法委书记", "start": "2020-12", "end": "2021?", "rank": "县处级副职", "note": ""},
    {"id": 4, "person_id": 2, "org_id": 14, "title": "梅州市委副秘书长、三级调研员", "start": "2018-12", "end": "2020-11", "rank": "处级", "note": ""},
    {"id": 5, "person_id": 2, "org_id": 13, "title": "梅州市政府研究室主任", "start": "2012-07", "end": "2018-12", "rank": "处级", "note": ""},
    {"id": 6, "person_id": 2, "org_id": 13, "title": "梅州市政府研究室副主任", "start": "2008-11", "end": "2012-07", "rank": "处级副职", "note": ""},
    {"id": 7, "person_id": 2, "org_id": 13, "title": "梅州市政府研究室研究二科科长", "start": "2005-02", "end": "2008-11", "rank": "乡科级", "note": ""},
    {"id": 8, "person_id": 2, "org_id": 12, "title": "丰顺县农业委员会科员、综合组副组长", "start": "1995-08", "end": "2002-10", "rank": "办事员", "note": ""},
    # ── 胡班 (县委副书记、政法委书记) ──
    {"id": 9, "person_id": 3, "org_id": 1, "title": "蕉岭县委副书记、政法委书记", "start": "2024-12", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 肖纯辉 (省派副书记) ──
    {"id": 10, "person_id": 4, "org_id": 1, "title": "蕉岭县委副书记（省纵向帮扶队长）", "start": "2024?", "end": "今", "rank": "县处级副职", "note": "省市场监管局下派"},
    # ── 徐永岭 (常务副县长) ──
    {"id": 11, "person_id": 5, "org_id": 2, "title": "蕉岭县委常委、常务副县长", "start": "2021-09", "end": "今", "rank": "县处级副职", "note": "现任"},
    {"id": 12, "person_id": 5, "org_id": 2, "title": "蕉岭县副县长", "start": "2017-08", "end": "2021-09", "rank": "县处级副职", "note": ""},
    {"id": 13, "person_id": 5, "org_id": 18, "title": "蕉岭县科工商务管理局局长", "start": "2015-01", "end": "2017-08", "rank": "乡科级正职", "note": ""},
    {"id": 14, "person_id": 5, "org_id": 17, "title": "蕉岭县文福镇党委书记、人大主席", "start": "2011-06", "end": "2014-12", "rank": "乡科级正职", "note": ""},
    {"id": 15, "person_id": 5, "org_id": 17, "title": "蕉岭县文福镇镇长", "start": "2006-08", "end": "2011-06", "rank": "乡科级正职", "note": ""},
    {"id": 16, "person_id": 5, "org_id": 16, "title": "蕉岭县蓝坊镇党委副书记、纪委书记", "start": "2004-04", "end": "2006-08", "rank": "乡科级副职", "note": ""},
    {"id": 17, "person_id": 5, "org_id": 23, "title": "蕉岭县北礤镇党委组织委员", "start": "2002-01", "end": "2004-04", "rank": "乡科级副职", "note": ""},
    {"id": 18, "person_id": 5, "org_id": 15, "title": "蕉岭县徐溪镇政府司法助理、计育办主任", "start": "1995-08", "end": "2002-01", "rank": "办事员", "note": ""},
    # ── 王映萍 (常委副县长) ──
    {"id": 19, "person_id": 6, "org_id": 2, "title": "蕉岭县委常委、副县长", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 黄鹏 (纪委书记) ──
    {"id": 20, "person_id": 7, "org_id": 3, "title": "蕉岭县委常委、纪委书记、监委主任", "start": "2024-09", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 谢伟传 (组织部长) ──
    {"id": 21, "person_id": 8, "org_id": 1, "title": "蕉岭县委常委、组织部部长", "start": "2025?", "end": "今", "rank": "县处级副职", "note": "现任，接替曹彦"},
    # ── 陈丽 (宣传部长) ──
    {"id": 22, "person_id": 9, "org_id": 1, "title": "蕉岭县委常委、宣传部部长", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 丘文慈 (县委办主任、统战部长) ──
    {"id": 23, "person_id": 10, "org_id": 1, "title": "蕉岭县委常委、县委办主任、统战部长", "start": "2020-08", "end": "今", "rank": "县处级副职", "note": "现任"},
    {"id": 24, "person_id": 10, "org_id": 20, "title": "蕉岭县政府办公室主任", "start": "2013-03", "end": "2019-05", "rank": "乡科级正职", "note": ""},
    {"id": 25, "person_id": 10, "org_id": 19, "title": "蕉岭县广福镇党委书记、人大主席", "start": "2010-10", "end": "2013-03", "rank": "乡科级正职", "note": ""},
    {"id": 26, "person_id": 10, "org_id": 19, "title": "蕉岭县广福镇镇长", "start": "2005-08", "end": "2010-10", "rank": "乡科级正职", "note": ""},
    # ── 王晓峰 (人武部) ──
    {"id": 27, "person_id": 11, "org_id": 8, "title": "蕉岭县委常委、县人武部", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 钟剑平 (副县长、公安局长) ──
    {"id": 28, "person_id": 12, "org_id": 2, "title": "蕉岭县副县长、县公安局局长", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 钟光庆 (副县长) ──
    {"id": 29, "person_id": 13, "org_id": 2, "title": "蕉岭县副县长", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 张慧 (副县长) ──
    {"id": 30, "person_id": 14, "org_id": 2, "title": "蕉岭县副县长", "start": "2026?", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 李杜强 (副县长) ──
    {"id": 31, "person_id": 15, "org_id": 2, "title": "蕉岭县副县长", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 周锐明 (副县长、帮扶队长) ──
    {"id": 32, "person_id": 16, "org_id": 2, "title": "蕉岭县副县长（番禺对口帮扶队长）", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 人大 ──
    {"id": 33, "person_id": 17, "org_id": 4, "title": "蕉岭县人大常委会主任", "start": "待查", "end": "今", "rank": "县处级正职", "note": "现任"},
    {"id": 34, "person_id": 18, "org_id": 4, "title": "蕉岭县人大常委会副主任", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    {"id": 35, "person_id": 19, "org_id": 4, "title": "蕉岭县人大常委会副主任", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    {"id": 36, "person_id": 20, "org_id": 4, "title": "蕉岭县人大常委会副主任", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    {"id": 37, "person_id": 21, "org_id": 4, "title": "蕉岭县人大常委会副主任、县总工会主席", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 政协 ──
    {"id": 38, "person_id": 22, "org_id": 5, "title": "蕉岭县政协主席", "start": "待查", "end": "今", "rank": "县处级正职", "note": "现任"},
    # ── 法检 ──
    {"id": 39, "person_id": 23, "org_id": 6, "title": "蕉岭县人民法院院长", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    {"id": 40, "person_id": 24, "org_id": 7, "title": "蕉岭县人民检察院检察长", "start": "待查", "end": "今", "rank": "县处级副职", "note": "现任"},
    # ── 纪委副书记 ──
    {"id": 41, "person_id": 25, "org_id": 3, "title": "蕉岭县纪委副书记、县监委副主任", "start": "待查", "end": "今", "rank": "乡科级正职", "note": "现任"},
]

relationships = [
    # ── 党政搭档 ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "刘鸿涛（县委书记）与刘裕君（县长）为蕉岭县党政正职搭档",
     "overlap_org": "中共蕉岭县委员会、蕉岭县人民政府",
     "overlap_period": "2021-2026"},
    # ── 县委副书记与书记 ──
    {"id": 2, "person_a_id": 3, "person_b_id": 1, "type": "同级领导",
     "context": "胡班（县委副书记、政法委书记）协助刘鸿涛分管县委日常工作",
     "overlap_org": "中共蕉岭县委员会",
     "overlap_period": "2024-2026"},
    # ── 常务副县长与县长 ──
    {"id": 3, "person_a_id": 5, "person_b_id": 2, "type": "上下级",
     "context": "徐永岭（常务副县长）协助刘裕君（县长）负责县政府日常工作",
     "overlap_org": "蕉岭县人民政府",
     "overlap_period": "2021-2026"},
    # ── 县委办与县委 ──
    {"id": 4, "person_a_id": 10, "person_b_id": 1, "type": "上下级",
     "context": "丘文慈（县委办主任）协助刘鸿涛处理县委日常事务",
     "overlap_org": "中共蕉岭县委员会",
     "overlap_period": "2020-2026"},
    # ── 人大与党委 ──
    {"id": 5, "person_a_id": 17, "person_b_id": 1, "type": "同级领导",
     "context": "张伟杰（人大主任）与刘鸿涛（县委书记）同县处级正职",
     "overlap_org": "蕉岭县",
     "overlap_period": ""},
    # ── 政协与党委 ──
    {"id": 6, "person_a_id": 22, "person_b_id": 1, "type": "同级领导",
     "context": "钟梅芬（政协主席）与刘鸿涛（县委书记）同县处级正职",
     "overlap_org": "蕉岭县",
     "overlap_period": ""},
    # ── 纪委与党委 ──
    {"id": 7, "person_a_id": 7, "person_b_id": 1, "type": "上下级",
     "context": "黄鹏（纪委书记）在县委和市纪委双重领导下工作",
     "overlap_org": "中共蕉岭县委员会",
     "overlap_period": "2024-2026"},
    # ── 副书记（省派）与书记 ──
    {"id": 8, "person_a_id": 4, "person_b_id": 1, "type": "上下级",
     "context": "肖纯辉（省派副书记）挂职协助刘鸿涛",
     "overlap_org": "中共蕉岭县委员会",
     "overlap_period": "2024-2026"},
    # ── 徐永岭与丘文慈（蕉岭本土干部交集） ──
    {"id": 9, "person_a_id": 5, "person_b_id": 10, "type": "同僚",
     "context": "徐永岭与丘文慈均为蕉岭本土成长干部，两人在蕉岭基层工作多年，存在工作交集",
     "overlap_org": "蕉岭县",
     "overlap_period": "1994-2026"},
    # ── 刘裕君与胡班（大埔县工作交集） ──
    {"id": 10, "person_a_id": 2, "person_b_id": 3, "type": "推测关联",
     "context": "刘裕君曾任大埔县委副书记、政法委书记，胡班现任蕉岭县委副书记、政法委书记，两人均从事政法/党务工作，需确认是否有直接交集",
     "overlap_org": "",
     "overlap_period": "2020-2021",
     "confidence": "plausible"},
    # ── 胡班与黄鹏（纪委/政法系统协作） ──
    {"id": 11, "person_a_id": 3, "person_b_id": 7, "type": "同僚",
     "context": "胡班（政法委书记）与黄鹏（纪委书记）在反腐败协调机制中需协作",
     "overlap_org": "中共蕉岭县委员会",
     "overlap_period": "2024-2026"},
    # ── 副县长与常务副县长 ──
    {"id": 12, "person_a_id": 5, "person_b_id": 12, "type": "上下级",
     "context": "徐永岭（常务副县长）统筹钟剑平（副县长、公安局长）等工作",
     "overlap_org": "蕉岭县人民政府",
     "overlap_period": ""},
    {"id": 13, "person_a_id": 5, "person_b_id": 13, "type": "上下级",
     "context": "徐永岭（常务副县长）统筹钟光庆（副县长）等工作",
     "overlap_org": "蕉岭县人民政府",
     "overlap_period": ""},
    {"id": 14, "person_a_id": 5, "person_b_id": 14, "type": "上下级",
     "context": "徐永岭（常务副县长）统筹张慧（副县长）等工作",
     "overlap_org": "蕉岭县人民政府",
     "overlap_period": ""},
    {"id": 15, "person_a_id": 5, "person_b_id": 15, "type": "上下级",
     "context": "徐永岭（常务副县长）统筹李杜强（副县长）等工作",
     "overlap_org": "蕉岭县人民政府",
     "overlap_period": ""},
    {"id": 16, "person_a_id": 5, "person_b_id": 16, "type": "上下级",
     "context": "徐永岭（常务副县长）统筹周锐明（副县长）等工作",
     "overlap_org": "蕉岭县人民政府",
     "overlap_period": ""},
    # ── 纪委书记与纪委副书记 ──
    {"id": 17, "person_a_id": 7, "person_b_id": 25, "type": "上下级",
     "context": "黄鹏（纪委书记）与李浩（纪委副书记）为纪委领导班子成员",
     "overlap_org": "中共蕉岭县纪律检查委员会",
     "overlap_period": ""},
    # ── 谢伟传（组织部）与常委班子 ──
    {"id": 18, "person_a_id": 8, "person_b_id": 10, "type": "同级领导",
     "context": "谢伟传（组织部长）与丘文慈（县委办主任）均为县委常委",
     "overlap_org": "中共蕉岭县委员会",
     "overlap_period": "2025-2026"},
    {"id": 19, "person_a_id": 8, "person_b_id": 9, "type": "同级领导",
     "context": "谢伟传（组织部长）与陈丽（宣传部长）均为县委常委",
     "overlap_org": "中共蕉岭县委员会",
     "overlap_period": "2025-2026"},
]

# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(STAGING_DB), exist_ok=True)
if os.path.exists(STAGING_DB):
    os.remove(STAGING_DB)

conn = sqlite3.connect(STAGING_DB)
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

# Summary
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]
conn.close()

print(f"SQLite database written: {STAGING_DB}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>蕉岭县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
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

# Nodes: Persons
party_sec_ids = {1}       # 刘鸿涛
gov_leader_ids = {2}      # 刘裕君
discipline_ids = {7}      # 黄鹏
top_leader_ids = {1, 2}   # larger size

lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    if pid in party_sec_ids:
        color = '#E03C31'  # Red: Party Secretary
        size = 20.0
    elif pid in gov_leader_ids:
        color = '#2980B9'  # Blue: Government leader
        size = 18.0
    elif pid in discipline_ids:
        color = '#E67E22'  # Orange: Discipline
        size = 16.0
    else:
        color = '#95A5A6'  # Grey: Others
        size = 12.0

    lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="person"/>')
    lines.append('          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append('        <viz:color r="44" g="62" b="80"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(pos["start"] or "?")} → {esc(pos["end"] or "今")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(STAGING_GEXF, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {STAGING_GEXF}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
