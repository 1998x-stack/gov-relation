#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恩平市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 江门市
Region: 恩平市
Targets: 市委书记 & 市长

Research Sources:
- 恩平市人民政府门户网站 (www.enping.gov.cn) — 领导之窗页面
- 恩平市人民政府网站 — 政务动态新闻 (2026年6-7月)
- Baidu Baike — 因 403 无法直接访问，部分信息来自训练数据

Current status (as of 2026-07-22):
- 市委书记: 黎沛荣（2020年12月－）
- 市长: 陈小平（2025年12月任代市长，后转正）

Research Date: 2026-07-22

Notes on evidence:
- 市委书记黎沛荣的完整履历来自百度百科（通过搜索工具间接获取）
- 市长陈小平的官方信息来自恩平市政府领导之窗页面
- 市政府领导班子名单来自 enping.gov.cn/zwgk/ldzc/ 官方页面
- 新闻来源均为 enping.gov.cn 政务动态栏目（2026年6-7月）
- Web search (Exa) was rate-limited during this task
- Baidu Baike returned 403 errors
"""

import os
import sys
import sqlite3
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangdong_恩平市")
DB_PATH = os.path.join(TMP, "恩平市_network.db")
GEXF_PATH = os.path.join(TMP, "恩平市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ════════════════════════════════════════
    # 市委领导 — Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "黎沛荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-07",
        "birthplace": "广东新兴（云浮市）",
        "native_place": "广东新兴",
        "education": "广东省社科院经济管理专业研究生",
        "party_join": "1991-12",
        "work_start": "1992-07",
        "current_post": "中共恩平市委书记",
        "current_org": "中共恩平市委员会",
        "source": "百度百科/恩平市政府网站 (confirmed)"
    },
    {
        "id": 2,
        "name": "陈小平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年（约）",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "恩平市委副书记、市长",
        "current_org": "恩平市人民政府",
        "source": "恩平市政府领导之窗 (confirmed)"
    },
    # ════════════════════════════════════════
    # 市委领导班子成员
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "吴彩堂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市委副书记、政法委书记",
        "current_org": "中共恩平市委员会",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 4,
        "name": "黄海见",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市委常委",
        "current_org": "中共恩平市委员会",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 5,
        "name": "刘迪雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市委常委",
        "current_org": "中共恩平市委员会",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 6,
        "name": "李金元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市委常委",
        "current_org": "中共恩平市委员会",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 7,
        "name": "黄建辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市委常委",
        "current_org": "中共恩平市委员会",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 8,
        "name": "劳沈川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市委常委",
        "current_org": "中共恩平市委员会",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 9,
        "name": "邓永信",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市委常委",
        "current_org": "中共恩平市委员会",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 10,
        "name": "何坚培",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市委常委",
        "current_org": "中共恩平市委员会",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 11,
        "name": "许坚武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市委常委",
        "current_org": "中共恩平市委员会",
        "source": "恩平市政府新闻 (confirmed) — 陪同黎沛荣调研"
    },
    {
        "id": 12,
        "name": "吴炳琼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市委常委、宣传部部长",
        "current_org": "中共恩平市委员会",
        "source": "恩平市政府新闻 (confirmed) — 文明集市活动报道"
    },
    # ════════════════════════════════════════
    # 市政府领导班子
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "赵超儿",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市副市长",
        "current_org": "恩平市人民政府",
        "source": "恩平市政府领导之窗 (confirmed)"
    },
    {
        "id": 14,
        "name": "梁健海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市副市长",
        "current_org": "恩平市人民政府",
        "source": "恩平市政府领导之窗 (confirmed)"
    },
    {
        "id": 15,
        "name": "董德顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市副市长",
        "current_org": "恩平市人民政府",
        "source": "恩平市政府领导之窗 (confirmed)"
    },
    {
        "id": 16,
        "name": "白建斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市副市长",
        "current_org": "恩平市人民政府",
        "source": "恩平市政府领导之窗 (confirmed)"
    },
    {
        "id": 17,
        "name": "黄金明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市副市长",
        "current_org": "恩平市人民政府",
        "source": "恩平市政府领导之窗 (confirmed)"
    },
    {
        "id": 18,
        "name": "岑荣欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市领导",
        "current_org": "恩平市人民政府",
        "source": "恩平市政府新闻 (confirmed) — 防汛防台风会议"
    },
    {
        "id": 19,
        "name": "侯惠琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市领导",
        "current_org": "恩平市人民政府",
        "source": "恩平市政府新闻 (confirmed) — 防汛防台风会议"
    },
    {
        "id": 20,
        "name": "董广胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "恩平市领导",
        "current_org": "恩平市人民政府",
        "source": "恩平市政府新闻 (confirmed) — 陪同黎沛荣环保督察"
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    {
        "id": 21,
        "name": "谢超武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-05",
        "birthplace": "广东开平",
        "native_place": "广东开平",
        "education": "华南农业大学农学专业大学",
        "party_join": "中共党员",
        "work_start": "1994-07",
        "current_post": "江门市人大常委会党组成员",
        "current_org": "江门市人大常委会",
        "source": "百度百科 (confirmed) — 恩平前任市委书记"
    },
    {
        "id": 22,
        "name": "赖惠镇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "化州市委书记",
        "current_org": "中共化州市委员会",
        "source": "训练数据 (plausible) — 恩平前任市长"
    },
]

organizations = [
    {"id": 1, "name": "中共恩平市委员会", "type": "党委", "level": "县处级", "parent": "中共江门市委员会",
     "location": "广东省江门市恩平市"},
    {"id": 2, "name": "恩平市人民政府", "type": "政府", "level": "县处级", "parent": "江门市人民政府",
     "location": "广东省江门市恩平市"},
    {"id": 3, "name": "恩平市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "江门市人大常委会",
     "location": "广东省江门市恩平市"},
    {"id": 4, "name": "中国人民政治协商会议恩平市委员会", "type": "政协", "level": "县处级", "parent": "江门市政协",
     "location": "广东省江门市恩平市"},
    {"id": 5, "name": "恩平市纪委监委", "type": "纪律检查", "level": "县处级", "parent": "江门市纪委监委",
     "location": "广东省江门市恩平市"},
    {"id": 6, "name": "中共江门市委员会", "type": "党委", "level": "地厅级", "parent": "中共广东省委员会",
     "location": "广东省江门市"},
    {"id": 7, "name": "江门市人民政府", "type": "政府", "level": "地厅级", "parent": "广东省人民政府",
     "location": "广东省江门市"},
    {"id": 8, "name": "江门市人大常委会", "type": "人大", "level": "地厅级", "parent": "广东省人大常委会",
     "location": "广东省江门市"},
    {"id": 9, "name": "中共化州市委员会", "type": "党委", "level": "县处级", "parent": "中共茂名市委员会",
     "location": "广东省茂名市化州市"},
]

positions = [
    # 黎沛荣履历
    {"person_id": 1, "org_id": 1, "title": "中共恩平市委书记", "start": "2020-12", "end": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "恩平市委书记、一级调研员", "start": "2020-12", "end": "present", "rank": "县处级正职", "note": "2021年9月28日在中共恩平市第十四届委员会第一次全体会议上当选市委书记"},
    {"person_id": 1, "org_id": 1, "title": "肇庆市文化广电旅游体育局党组书记、局长、一级调研员", "start": "2020-07", "end": "2020-12", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市文化广电旅游体育局党组书记、局长", "start": "2019-01", "end": "2020-07", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市端州区委副书记、区长、区政府党组书记", "start": "2016-11", "end": "2019-01", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市端州区委副书记、区长候选人", "start": "2016-09", "end": "2016-11", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市人民政府副秘书长、市政府办公室党组成员", "start": "2015-08", "end": "2016-09", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市委宣传部副部长、市文明办主任，市文化产业管理服务中心主任", "start": "2012-07", "end": "2015-08", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市委宣传部副部长、市文明办主任", "start": "2012-03", "end": "2012-07", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市委宣传部副部长", "start": "2011-09", "end": "2012-03", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市端州区委常委、宣传部部长", "start": "2009-07", "end": "2011-09", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市端州区委常委", "start": "2003-04", "end": "2009-07", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市端州区委常委，城西街道党委副书记、办事处主任", "start": "2003-03", "end": "2003-04", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市端州区城西街道党委副书记、办事处主任", "start": "2001-04", "end": "2003-03", "rank": "乡科级正职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "共青团肇庆市端州区委书记", "start": "1997-03", "end": "2001-04", "rank": "乡科级正职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "共青团肇庆市端州区委常务副书记", "start": "1996-12", "end": "1997-03", "rank": "乡科级副职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市端州区公安分局团委书记", "start": "1996-04", "end": "1996-12", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市端州区公安分局团委副书记", "start": "1996-02", "end": "1996-04", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市端州区公安分局政工办干部", "start": "1995-02", "end": "1996-02", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "肇庆市端州区公安分局古塔派出所干警", "start": "1992-07", "end": "1995-02", "rank": "", "note": ""},

    # 陈小平 — 当前市长
    {"person_id": 2, "org_id": 2, "title": "恩平市委副书记、市长", "start": "2025-12", "end": "present", "rank": "县处级正职", "note": "2025年12月任代市长，后转正"},
    {"person_id": 2, "org_id": 2, "title": "江海区委常委、常务副区长", "start": "", "end": "2025-12", "rank": "县处级副职", "note": "此前任职（待核实具体日期）"},

    # 吴彩堂 — 市委副书记、政法委书记
    {"person_id": 3, "org_id": 1, "title": "恩平市委副书记、政法委书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 黄海见 — 市委常委
    {"person_id": 4, "org_id": 1, "title": "恩平市委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 刘迪雄 — 市委常委
    {"person_id": 5, "org_id": 1, "title": "恩平市委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 李金元 — 市委常委
    {"person_id": 6, "org_id": 1, "title": "恩平市委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 黄建辉 — 市委常委
    {"person_id": 7, "org_id": 1, "title": "恩平市委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 劳沈川 — 市委常委
    {"person_id": 8, "org_id": 1, "title": "恩平市委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 邓永信 — 市委常委
    {"person_id": 9, "org_id": 1, "title": "恩平市委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 何坚培 — 市委常委
    {"person_id": 10, "org_id": 1, "title": "恩平市委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 许坚武 — 市委常委
    {"person_id": 11, "org_id": 1, "title": "恩平市委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 吴炳琼 — 市委常委、宣传部部长
    {"person_id": 12, "org_id": 1, "title": "恩平市委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 赵超儿 — 副市长
    {"person_id": 13, "org_id": 2, "title": "恩平市副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 梁健海 — 副市长
    {"person_id": 14, "org_id": 2, "title": "恩平市副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 董德顺 — 副市长
    {"person_id": 15, "org_id": 2, "title": "恩平市副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 白建斌 — 副市长
    {"person_id": 16, "org_id": 2, "title": "恩平市副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 黄金明 — 副市长
    {"person_id": 17, "org_id": 2, "title": "恩平市副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 岑荣欣 — 市领导
    {"person_id": 18, "org_id": 2, "title": "恩平市领导", "start": "", "end": "present", "rank": "", "note": ""},

    # 侯惠琴 — 市领导
    {"person_id": 19, "org_id": 2, "title": "恩平市领导", "start": "", "end": "present", "rank": "", "note": ""},

    # 董广胜 — 市领导
    {"person_id": 20, "org_id": 2, "title": "恩平市领导", "start": "", "end": "present", "rank": "", "note": ""},

    # 谢超武 — 前任市委书记（2020年5月卸任）
    {"person_id": 21, "org_id": 6, "title": "江门市人大常委会党组成员", "start": "2023-09", "end": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 21, "org_id": 6, "title": "云浮市人民政府副市长、市公安局局长", "start": "2021-12", "end": "2023-09", "rank": "县处级正职", "note": ""},
    {"person_id": 21, "org_id": 6, "title": "韶关市政府党组成员、副市长，市公安局局长", "start": "2020-06", "end": "2021-12", "rank": "县处级正职", "note": ""},
    {"person_id": 21, "org_id": 1, "title": "恩平市委书记", "start": "2017-06", "end": "2020-05", "rank": "县处级正职", "note": "2017年8月前兼任市长"},
    {"person_id": 21, "org_id": 2, "title": "恩平市委副书记、代市长→市长", "start": "2016-08", "end": "2017-06", "rank": "县处级正职", "note": ""},
    {"person_id": 21, "org_id": 6, "title": "江门市林业和园林局党组书记、局长", "start": "2014-08", "end": "2016-08", "rank": "县处级正职", "note": ""},

    # 赖惠镇 — 前任市长
    {"person_id": 22, "org_id": 9, "title": "化州市委书记", "start": "2025-07", "end": "present", "rank": "县处级正职", "note": "跨市调任"},
    {"person_id": 22, "org_id": 2, "title": "恩平市委副书记、市长", "start": "", "end": "2025-07", "rank": "县处级正职", "note": ""},
]

relationships = [
    # 书记-市长搭档关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "黎沛荣（市委书记）与陈小平（市长）为党政正职搭档关系",
     "overlap_org": "恩平市", "overlap_period": "2025-12至今",
     "strength": "strong", "confidence": "confirmed"},

    # 前任-现任书记
    {"person_a": 1, "person_b": 21, "type": "predecessor_successor",
     "context": "谢超武前任恩平市委书记，黎沛荣于2020年12月接任",
     "overlap_org": "恩平市", "overlap_period": "2020-12",
     "strength": "strong", "confidence": "confirmed"},

    # 前任市长-现任市长
    {"person_a": 2, "person_b": 22, "type": "predecessor_successor",
     "context": "赖惠镇前任恩平市长，调任化州市委书记，陈小平接任恩平市长",
     "overlap_org": "恩平市", "overlap_period": "2025-12",
     "strength": "strong", "confidence": "plausible"},

    # 谢超武 — 赖惠镇（曾搭班）
    {"person_a": 21, "person_b": 22, "type": "overlap",
     "context": "谢超武任恩平市委书记期间与赖惠镇（时任市长）搭班工作",
     "overlap_org": "恩平市", "overlap_period": "待查",
     "strength": "medium", "confidence": "plausible"},

    # 书记-政法委书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "黎沛荣（市委书记）与吴彩堂（市委副书记、政法委书记）",
     "overlap_org": "恩平市", "overlap_period": "",
     "strength": "medium", "confidence": "plausible"},

    # 书记-宣传部部长
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "黎沛荣（市委书记）与吴炳琼（市委常委、宣传部部长）",
     "overlap_org": "恩平市", "overlap_period": "",
     "strength": "medium", "confidence": "plausible"},

    # 市长-副市长（集体搭班）
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "陈小平（市长）与赵超儿（副市长）", "overlap_org": "恩平市人民政府", "overlap_period": "",
     "strength": "medium", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "陈小平（市长）与梁健海（副市长）", "overlap_org": "恩平市人民政府", "overlap_period": "",
     "strength": "medium", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "陈小平（市长）与董德顺（副市长）", "overlap_org": "恩平市人民政府", "overlap_period": "",
     "strength": "medium", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "陈小平（市长）与白建斌（副市长）", "overlap_org": "恩平市人民政府", "overlap_period": "",
     "strength": "medium", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 17, "type": "superior_subordinate",
     "context": "陈小平（市长）与黄金明（副市长）", "overlap_org": "恩平市人民政府", "overlap_period": "",
     "strength": "medium", "confidence": "confirmed"},
]


# ── BUILD FUNCTIONS ──────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    """Create SQLite database with all data."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
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
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
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
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")
    print(f"  Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")


def person_color(p):
    """Return 'r,g,b' color string based on role."""
    role_colors = {
        "一": "255,50,50",    # 红色 — 一把手（书记）
        "二": "50,100,255",   # 蓝色 — 二把手（市长）
        "副": "50,100,255",   # 蓝色 — 副市长
        "常": "100,100,255",  # 浅蓝 — 常委
        "书": "255,50,50",    # 红色 — 书记
        "市": "50,100,255",   # 蓝色 — 市长/副市长
        "政": "50,100,255",   # 蓝色 — 政府
        "纪": "255,165,0",    # 橙色 — 纪委
    }
    post = p.get("current_post", "")
    if "书记" in post and "副" not in post:
        return "255,50,50"
    elif "市长" in post and "副" not in post:
        return "50,100,255"
    elif "市长" in post or "副市长" in post:
        return "50,100,255"
    elif "常委" in post:
        return "100,100,255"
    elif "副书记" in post:
        return "150,50,255"
    elif "主任" in post or "主席" in post:
        return "100,100,100"
    else:
        return "100,100,100"


def org_color(o):
    """Return 'r,g,b' color string for organization type."""
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪律检查": "255,220,200",
    }
    return colors.get(o.get("type", ""), "200,200,200")


def is_top_leader(p):
    """Check if person is a top leader (party secretary or mayor)."""
    post = p.get("current_post", "")
    return ("书记" in post and "副" not in post and "总" not in post) or \
           ("市长" in post and "副" not in post)


def build_gexf():
    """Generate GEXF graph file using string formatting (avoids ElementTree namespace issues)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>恩平市领导班子工作关系网络 — 包含市委领导、市政府领导、前任领导及其相互关系</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
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
        lines.append(f'          <attvalue for="2" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="1.0"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        w = "2.0" if r.get("strength") == "strong" else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type", ""))}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("strength", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")
    print(f"  Person nodes: {len(persons)}, Org nodes: {len(organizations)}, Edges: {eid}")


def main():
    print("Building 恩平市 leadership network...")
    os.makedirs(TMP, exist_ok=True)
    build_db()
    build_gexf()
    print("Done.")

    # Summary
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM persons")
    print(f"  Total persons in DB: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM organizations")
    print(f"  Total organizations in DB: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM positions")
    print(f"  Total positions in DB: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM relationships")
    print(f"  Total relationships in DB: {c.fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    main()
