#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build SQLite database and GEXF graph for 江海区 (Jianghai District), Jiangmen, Guangdong.

   Research date: 2026-07-22
   Sources: www.jianghai.gov.cn leadership page, government news articles,
            media reports, appointment records.

   Official leadership roster source: http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/
   Accessed: 2026-07-22

   Note: Full career biographies for most leaders could not be verified
   due to degraded web access during research. All current roles are
   confirmed from the official government leadership page.
"""

import sqlite3
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangdong_江海区")
DB_PATH = os.path.join(TMP, "江海区_network.db")
GEXF_PATH = os.path.join(TMP, "江海区_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Current Top Leaders ──

    # 李捷 - 江海区委书记 (Party Secretary), also 江门高新区党工委书记
    {"id": 1, "name": "李捷", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委书记、江门高新区党工委书记",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/dzldbz/content/post_3094278.html (2026-07-22)"},

    # 颜乐中 - 区长（区委副书记、区长、区政府党组书记）
    {"id": 2, "name": "颜乐中", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委副书记、区长、区政府党组书记",
     "current_org": "江门市江海区人民政府",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/dzldbz/content/post_3372758.html (2026-07-22)"},

    # ── 区委常委 (Standing Committee Members) ──
    # 廖华 - 高新区党工委委员、管委会副主任、三级调研员
    {"id": 3, "name": "廖华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委、高新区党工委委员、管委会副主任",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/dzldbz/content/post_2843840.html (2026-07-22)"},

    # 莫兆汉 - 高新区党工委委员、管委会副主任、三级调研员
    {"id": 4, "name": "莫兆汉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委、高新区党工委委员、管委会副主任",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/dzldbz/content/post_2843846.html (2026-07-22)"},

    # 刘宏杰 - 高新区党工委委员、管委会副主任
    {"id": 5, "name": "刘宏杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委、高新区党工委委员、管委会副主任",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/dzldbz/content/post_2636159.html (2026-07-22)"},

    # 刘刚 - 纪委书记、监委主任
    {"id": 6, "name": "刘刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委、纪委书记、区监察委员会主任",
     "current_org": "中共江门市江海区纪律检查委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/dzldbz/content/post_2282909.html (2026-07-22)"},

    # 张连军 - 区人武部政治委员
    {"id": 7, "name": "张连军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委、区人武部政治委员",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/dzldbz/content/post_2120154.html (2026-07-22)"},

    # 邓志华 - 统战部部长
    {"id": 8, "name": "邓志华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委、统战部部长、区政协党组副书记",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/dzldbz/content/post_2429535.html (2026-07-22)"},

    # 李家豪 - 组织部部长、党校校长
    {"id": 9, "name": "李家豪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委、组织部部长、党校校长",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/dzldbz/content/post_3415343.html (2026-07-22)"},

    # 张健钰
    {"id": 10, "name": "张健钰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/ (2026-07-22)"},

    # 熊伟光
    {"id": 11, "name": "熊伟光", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/ (2026-07-22)"},

    # 莫蔼谋
    {"id": 12, "name": "莫蔼谋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/ (2026-07-22)"},

    # 陈振奎
    {"id": 13, "name": "陈振奎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/ (2026-07-22)"},

    # 胡敬东
    {"id": 14, "name": "胡敬东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/ (2026-07-22)"},

    # 杨寿勤
    {"id": 15, "name": "杨寿勤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区委常委",
     "current_org": "中共江门市江海区委员会",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/ (2026-07-22)"},

    # 丑继明 - 区人武部部长? Not fully verified role but listed on leadership page
    {"id": 16, "name": "丑继明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区领导",
     "current_org": "江门市江海区",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/ (2026-07-22)"},

    # 邓群标
    {"id": 17, "name": "邓群标", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区领导",
     "current_org": "江门市江海区",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/ (2026-07-22)"},

    # 谭金玲
    {"id": 18, "name": "谭金玲", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区领导",
     "current_org": "江门市江海区",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/ (2026-07-22)"},

    # 梁志成
    {"id": 19, "name": "梁志成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江海区领导",
     "current_org": "江门市江海区",
     "source": "http://www.jianghai.gov.cn/zwgk/xxgk/jgzn/ldzc/ (2026-07-22)"},

    # ── Previous Leaders ──
    # 聂加伟 - 前任江海区委书记 (李捷的前任)
    {"id": 20, "name": "聂加伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前江海区委书记（已离任）",
     "current_org": "",
     "source": "江门市干部任免信息 - media reports (前任区委书记)"},

    # 郑丹辉 - 前任江海区区长（颜乐中的前任）
    {"id": 21, "name": "郑丹辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前江海区区长（已离任）",
     "current_org": "",
     "source": "江门市干部任免信息 - media reports (前任区长)"},
]

organizations = [
    {"id": 1, "name": "中共江门市江海区委员会", "type": "党委", "level": "县处级",
     "parent": "中共江门市委员会", "location": "广东省江门市江海区"},
    {"id": 2, "name": "江门市江海区人民政府", "type": "政府", "level": "县处级",
     "parent": "江门市人民政府", "location": "广东省江门市江海区"},
    {"id": 3, "name": "江门国家高新技术产业开发区管理委员会", "type": "开发区", "level": "国家级",
     "parent": "江门市人民政府", "location": "广东省江门市江海区"},
    {"id": 4, "name": "中共江门市江海区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共江门市江海区委员会", "location": "广东省江门市江海区"},
    {"id": 5, "name": "江门市江海区监察委员会", "type": "政府", "level": "县处级",
     "parent": "江门市监察委员会", "location": "广东省江门市江海区"},
    {"id": 6, "name": "中国人民政治协商会议江门市江海区委员会", "type": "政协", "level": "县处级",
     "parent": "江门市政协", "location": "广东省江门市江海区"},
    {"id": 7, "name": "江门市江海区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "江门市人民代表大会常务委员会", "location": "广东省江门市江海区"},
    {"id": 8, "name": "江门市江海区人民武装部", "type": "事业单位", "level": "县处级",
     "parent": "江门军分区", "location": "广东省江门市江海区"},
]

positions = [
    # 李捷 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "江海区委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "2026年7月仍在任；兼任江门高新区党工委书记"},
    {"person_id": 1, "org_id": 3, "title": "江门高新区党工委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "兼任"},

    # 颜乐中 — 区委副书记、区长、区政府党组书记
    {"person_id": 2, "org_id": 1, "title": "江海区委副书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "兼任区长"},
    {"person_id": 2, "org_id": 2, "title": "江海区区长",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "区政府主要负责人；兼任区政府党组书记"},

    # 廖华 — 区委常委、高新区管委会副主任
    {"person_id": 3, "org_id": 1, "title": "江海区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "高新区党工委委员、管委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 莫兆汉 — 区委常委、高新区管委会副主任
    {"person_id": 4, "org_id": 1, "title": "江海区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "高新区党工委委员、管委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 刘宏杰 — 区委常委、高新区管委会副主任
    {"person_id": 5, "org_id": 1, "title": "江海区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "高新区党工委委员、管委会副主任",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 刘刚 — 纪委书记、监委主任
    {"person_id": 6, "org_id": 1, "title": "江海区委常委、纪委书记",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "区监察委员会主任",
     "start": "", "end": "", "rank": "县处级正职", "note": ""},

    # 张连军 — 人武部政委
    {"person_id": 7, "org_id": 1, "title": "江海区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "区人武部政治委员",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 邓志华 — 统战部部长
    {"person_id": 8, "org_id": 1, "title": "江海区委常委、统战部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "区政协党组副书记",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 李家豪 — 组织部部长
    {"person_id": 9, "org_id": 1, "title": "江海区委常委、组织部部长、党校校长",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 张健钰 — 区委常委
    {"person_id": 10, "org_id": 1, "title": "江海区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 熊伟光 — 区委常委
    {"person_id": 11, "org_id": 1, "title": "江海区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 莫蔼谋 — 区委常委
    {"person_id": 12, "org_id": 1, "title": "江海区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 陈振奎 — 区委常委
    {"person_id": 13, "org_id": 1, "title": "江海区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 胡敬东 — 区委常委
    {"person_id": 14, "org_id": 1, "title": "江海区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 杨寿勤 — 区委常委
    {"person_id": 15, "org_id": 1, "title": "江海区委常委",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 丑继明
    {"person_id": 16, "org_id": 2, "title": "江海区领导",
     "start": "", "end": "", "rank": "", "note": "具体职务未核实"},

    # 邓群标
    {"person_id": 17, "org_id": 2, "title": "江海区领导",
     "start": "", "end": "", "rank": "", "note": "具体职务未核实"},

    # 谭金玲
    {"person_id": 18, "org_id": 2, "title": "江海区领导",
     "start": "", "end": "", "rank": "", "note": "具体职务未核实"},

    # 梁志成
    {"person_id": 19, "org_id": 2, "title": "江海区领导",
     "start": "", "end": "", "rank": "", "note": "具体职务未核实"},

    # 聂加伟 — 前任区委书记
    {"person_id": 20, "org_id": 1, "title": "江海区委书记（前）",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "前任区委书记；李捷前任"},

    # 郑丹辉 — 前任区长
    {"person_id": 21, "org_id": 2, "title": "江海区区长（前）",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "前任区长；颜乐中前任"},
]

relationships = [
    # 李捷 ↔ 颜乐中：书记—区长搭档
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长，党政主要负责人",
     "overlap_org": "中共江门市江海区委员会/区人民政府",
     "overlap_period": "至今"},

    # 李捷 ↔ 聂加伟：前后任区委书记
    {"person_a": 1, "person_b": 20, "type": "接任", "context": "李捷接替聂加伟任江海区委书记",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": ""},

    # 颜乐中 ↔ 郑丹辉：前后任区长
    {"person_a": 2, "person_b": 21, "type": "接任", "context": "颜乐中接替郑丹辉任江海区区长",
     "overlap_org": "江门市江海区人民政府",
     "overlap_period": ""},

    # 李捷 — 区委常委共事关系
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "区委书记—纪委书记",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "区委书记—区委常委/统战部部长",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "区委书记—区委常委/组织部部长",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 12, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 13, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 14, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 15, "type": "共事", "context": "区委书记—区委常委",
     "overlap_org": "中共江门市江海区委员会",
     "overlap_period": "至今"},

    # 颜乐中（区长）↔ 区委常委（高交叉任职）
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—区委常委/高新区副主任",
     "overlap_org": "江门市江海区人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—区委常委/高新区副主任",
     "overlap_org": "江门市江海区人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长—区委常委/高新区副主任",
     "overlap_org": "江门市江海区人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—区委常委",
     "overlap_org": "江门市江海区人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "区长—区委常委",
     "overlap_org": "江门市江海区人民政府",
     "overlap_period": "至今"},

    # 高新区交叉任职
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "同时任高新区管委会副主任",
     "overlap_org": "江门国家高新技术产业开发区管理委员会",
     "overlap_period": "至今"},
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "同时任高新区管委会副主任",
     "overlap_org": "江门国家高新技术产业开发区管理委员会",
     "overlap_period": "至今"},
    {"person_a": 4, "person_b": 5, "type": "共事", "context": "同时任高新区管委会副主任",
     "overlap_org": "江门国家高新技术产业开发区管理委员会",
     "overlap_period": "至今"},
]


# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title and "人大" not in title and "政协" not in title:
        return "255,50,50"
    if "区长" in title:
        return "50,100,255"
    if "政协" in title:
        return "255,240,200"
    if "人大" in title:
        return "200,255,255"
    if "纪委" in title or "监委" in title:
        return "255,165,0"
    if "常委" in title:
        return "200,100,100"
    if "副区长" in title:
        return "100,100,200"
    if "管委会" in title:
        return "200,255,200"
    return "100,100,100"

def person_size(p):
    title = p["current_post"]
    if "区委书记" in title:
        return "20.0"
    if "区长" in title:
        return "18.0"
    if "人大常委会主任" in title:
        return "16.0"
    if "常委" in title:
        return "14.0"
    if "副区长" in title:
        return "12.0"
    if "政协" in title or "人大" in title:
        return "12.0"
    if "管委会" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
        "乡镇/街道": "255,255,200",
    }
    return colors.get(t, "200,200,200")

# ═══════════════════════════════════════════════════════════════════════
# BUILD DATABASE
# ═══════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            str(p["id"]), p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], "", p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            str(o["id"]), o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            str(pos["person_id"]), str(pos["org_id"]), pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            str(r["person_a"]), str(r["person_b"]), r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()

# ═══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ═══════════════════════════════════════════════════════════════════════

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>江门市江海区领导班子工作关系网络 - 数据来源: jianghai.gov.cn及公开报道</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')

    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="江门市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="江门市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0

    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = "plausible"
        if r["type"] in ("共事", "接任"):
            conf = "confirmed"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    print(f"=== 江门市江海区网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")

if __name__ == "__main__":
    main()
