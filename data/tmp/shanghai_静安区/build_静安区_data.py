#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 上海市静安区 leadership network.

调查日期: 2026-07-25
信息来源: 上海市静安区人民政府门户网站 (www.jingan.gov.cn)
调查级别: 市辖区(直辖市)

Confirmed from government homepage (2026-07):
- 钟晓咏 — 静安区委书记
- 翟磊 — 静安区委副书记、区长
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "静安区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "静安区_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "上海市静安区"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════════════════════
    # 区委领导 (District Party Committee)
    # ═══════════════════════════════════════════════

    # 区委书记 — 钟晓咏
    {
        "id": 1,
        "name": "钟晓咏",
        "gender": "男",
        "ethnicity": "畲族",
        "birth": "1972-10",
        "birthplace": "",
        "education": "在职研究生，法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共上海市静安区委书记",
        "current_org": "中共上海市静安区委员会",
        "source": "https://www.jingan.gov.cn/sy/004015/004015001/004015001001/20241221/e1b47321-42d1-4d59-864c-aaee96aaee97.html",
    },
    # 区委副书记、区长 — 翟磊
    {
        "id": 2,
        "name": "翟磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-02",
        "birthplace": "",
        "education": "在职研究生，法学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区委副书记、区长",
        "current_org": "上海市静安区人民政府",
        "source": "https://www.jingan.gov.cn/sy/004015/004015001/004015001002/20240606/7fbd3f02-b8e8-4bfd-a415-fa653609fddb.html",
    },
    # 区委副书记 — 徐静
    {
        "id": 3,
        "name": "徐静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971-11",
        "birthplace": "",
        "education": "大学，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区委副书记，区委党校校长，一级巡视员",
        "current_org": "中共上海市静安区委员会",
        "source": "https://www.jingan.gov.cn/sy/004015/004015001/004015001002/20240606/f0f644c8-2f49-43b0-8e3b-982fe5e2b6a5.html",
    },
    # 区委常委、政法委书记 — 王翔
    {
        "id": 4,
        "name": "王翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-12",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区委常委、政法委书记，一级巡视员",
        "current_org": "中共上海市静安区委政法委员会",
        "source": "https://www.jingan.gov.cn/sy/004015/004015001/004015001003/20211101/8c006412-0b66-4cf0-88e2-06d58b2daa23.html",
    },
    # 区委常委、纪委书记、监委主任 — 竺晓忠
    {
        "id": 5,
        "name": "竺晓忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-11",
        "birthplace": "",
        "education": "市委党校研究生，理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区委常委、区纪委书记，区监察委主任，一级巡视员",
        "current_org": "中共上海市静安区纪律检查委员会",
        "source": "https://www.jingan.gov.cn/sy/004015/004015001/004015001003/20241203/661d4672-c2e6-42a6-aed0-97c7638cd4e4.html",
    },
    # 区委常委、组织部部长 — 莫亮金
    {
        "id": 6,
        "name": "莫亮金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-07",
        "birthplace": "",
        "education": "在职研究生，管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区委常委、组织部部长",
        "current_org": "中共上海市静安区委组织部",
        "source": "https://www.jingan.gov.cn/sy/004015/004015001/004015001003/20211101/a68ef1fb-9c0b-4c4e-83e8-5706729d4a10.html",
    },
    # 区委常委、常务副区长 — 傅俊
    {
        "id": 7,
        "name": "傅俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-02",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区委常委、常务副区长，区政府党组副书记，区行政学院院长",
        "current_org": "上海市静安区人民政府",
        "source": "https://www.jingan.gov.cn/sy/004015/004015001/004015001003/20211101/e7b8c12e-fc22-4529-ac1a-fb3dc35e20c6.html",
    },
    # 区委常委、副区长 — 梅广清
    {
        "id": 8,
        "name": "梅广清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-05",
        "birthplace": "",
        "education": "研究生，工学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区委常委、副区长，一级巡视员",
        "current_org": "上海市静安区人民政府",
        "source": "https://www.jingan.gov.cn/sy/004015/004015001/004015001003/20200724/a3c1aa8e-a0df-4a34-bafd-834f6dbb0b24.html",
    },
    # 区委常委、区人民武装部政治委员 — 陈志忠
    {
        "id": 9,
        "name": "陈志忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-02",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区委常委、区人民武装部政治委员",
        "current_org": "上海市静安区人民武装部",
        "source": "https://www.jingan.gov.cn/sy/004015/004015001/004015001003/20230802/6b51bc04-8482-464c-928e-aaeb3a442163.html",
    },
    # 区委常委、宣传部部长 — 萧烨璎
    {
        "id": 10,
        "name": "萧烨璎",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-02",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区委常委、宣传部部长",
        "current_org": "中共上海市静安区委宣传部",
        "source": "https://www.jingan.gov.cn/sy/004015/004015001/004015001003/20240606/64e27fc8-0b1f-4ca7-8da2-72da67e7be1b.html",
    },
    # ═══════════════════════════════════════════════
    # 区政府副区长 (District Government)
    # ═══════════════════════════════════════════════

    # 副区长 — 龙婉丽
    {
        "id": 11,
        "name": "龙婉丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969-10",
        "birthplace": "",
        "education": "研究生，经济学博士",
        "party_join": "民盟",
        "work_start": "",
        "current_post": "静安区副区长，区红十字会会长",
        "current_org": "上海市静安区人民政府",
        "source": "https://www.jingan.gov.cn/sy/004015/004015003/004015003002/20210309/cd7f8510-f3c2-45db-abb7-f9fda27ea05f.html",
    },
    # 副区长 — 姜坚 (公安)
    {
        "id": 12,
        "name": "姜坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区副区长，市公安局静安分局党委书记、局长、督察长",
        "current_org": "上海市静安区人民政府",
        "source": "https://www.jingan.gov.cn/sy/004015/004015003/004015003002/20211101/47ce6d6e-5560-478d-b5cb-3fd9e6ffe0fe.html",
    },
    # 副区长 — 张军 (援疆)
    {
        "id": 13,
        "name": "张军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-12",
        "birthplace": "",
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区副区长，上海市对口支援新疆工作前方指挥部（第十一批）副总指挥",
        "current_org": "上海市静安区人民政府",
        "source": "https://www.jingan.gov.cn/sy/004015/004015003/004015003002/20191011/0bf981bc-64b4-44d6-be8c-947f5878a013.html",
    },
    # 副区长 — 胡勇
    {
        "id": 14,
        "name": "胡勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-08",
        "birthplace": "",
        "education": "研究生，经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区副区长",
        "current_org": "上海市静安区人民政府",
        "source": "https://www.jingan.gov.cn/sy/004015/004015003/004015003002/20250416/05191662-7cd5-401b-a208-34a62858a202.html",
    },
    # 副区长 — 施煜
    {
        "id": 15,
        "name": "施煜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-02",
        "birthplace": "",
        "education": "在职研究生，工学硕士，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区副区长",
        "current_org": "上海市静安区人民政府",
        "source": "https://www.jingan.gov.cn/sy/004015/004015003/004015003002/20251128/29cec589-edea-42b9-a9ff-98128042371f.html",
    },
    # ═══════════════════════════════════════════════
    # 人大、政协领导
    # ═══════════════════════════════════════════════

    # 区人大常委会主任 — 顾云豪
    {
        "id": 16,
        "name": "顾云豪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区人大常委会主任",
        "current_org": "上海市静安区人民代表大会常务委员会",
        "source": "https://www.jingan.gov.cn/sy/004015/004015002/004015002001/20190117/e6335d42-0fd9-4e12-9c72-34a60822a185.html",
    },
    # 区政协主席 — 丁宝定
    {
        "id": 17,
        "name": "丁宝定",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "静安区政协主席",
        "current_org": "中国人民政治协商会议上海市静安区委员会",
        "source": "https://www.jingan.gov.cn/sy/004015/004015004/004015004001/20190801/eea5bd82-3814-4a47-b37d-15b970d37343.html",
    },
    # ═══════════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ═══════════════════════════════════════════════

    # 前任区委书记 — 于勇 (前任)
    {
        "id": 18,
        "name": "于勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-01",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/",
    },
    # 前任区长 — 王华 (前任)
    {
        "id": 19,
        "name": "王华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "江苏靖江",
        "education": "上海交通大学硕士研究生",
        "party_join": "中共党员",
        "work_start": "1996-08",
        "current_post": "徐汇区委副书记、区长",
        "current_org": "上海市徐汇区人民政府",
        "source": "https://www.xuhui.gov.cn/",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共上海市静安区委员会", "type": "党委", "level": "市辖区(直辖市)", "parent": "中共上海市委", "location": "上海市静安区"},
    {"id": 2, "name": "上海市静安区人民政府", "type": "政府", "level": "市辖区(直辖市)", "parent": "上海市人民政府", "location": "上海市静安区"},
    {"id": 3, "name": "中共上海市静安区纪律检查委员会", "type": "纪委", "level": "市辖区(直辖市)", "parent": "中共上海市静安区委员会", "location": "上海市静安区"},
    {"id": 4, "name": "中共上海市静安区委政法委员会", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市静安区委员会", "location": "上海市静安区"},
    {"id": 5, "name": "中共上海市静安区委组织部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市静安区委员会", "location": "上海市静安区"},
    {"id": 6, "name": "中共上海市静安区委宣传部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市静安区委员会", "location": "上海市静安区"},
    {"id": 7, "name": "上海市静安区人民武装部", "type": "军队", "level": "市辖区(直辖市)", "parent": "上海警备区", "location": "上海市静安区"},
    {"id": 8, "name": "上海市静安区人民代表大会常务委员会", "type": "人大", "level": "市辖区(直辖市)", "parent": "上海市人民代表大会常务委员会", "location": "上海市静安区"},
    {"id": 9, "name": "中国人民政治协商会议上海市静安区委员会", "type": "政协", "level": "市辖区(直辖市)", "parent": "中国人民政治协商会议上海市委员会", "location": "上海市静安区"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 钟晓咏
    {"person_id": 1, "org_id": 1, "title": "中共上海市静安区委书记", "start_date": "2024-12", "end_date": "present", "rank": "正厅级", "note": "2024年12月任静安区委书记；此前任徐汇区委副书记、区长"},
    {"person_id": 1, "org_id": 2, "title": "上海市徐汇区委副书记、区长", "start_date": "2019", "end_date": "2023-03", "rank": "正厅级", "note": "此前任徐汇区委常委、副区长"},
    # 翟磊
    {"person_id": 2, "org_id": 2, "title": "静安区委副书记、区长，区政府党组书记", "start_date": "2024-06", "end_date": "present", "rank": "正厅级", "note": "2024年6月任静安区代区长，后任区长"},
    {"person_id": 2, "org_id": 2, "title": "上海市浦东新区副区长", "start_date": "2021", "end_date": "2024", "rank": "副厅级", "note": "曾任浦东新区副区长、中国（上海）自由贸易试验区管委会副主任"},
    # 徐静
    {"person_id": 3, "org_id": 1, "title": "静安区委副书记，区委党校校长，一级巡视员", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 王翔
    {"person_id": 4, "org_id": 4, "title": "静安区委常委、政法委书记，一级巡视员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 竺晓忠
    {"person_id": 5, "org_id": 3, "title": "静安区委常委、区纪委书记，区监察委主任，一级巡视员", "start_date": "2024-12", "end_date": "present", "rank": "副厅级", "note": ""},
    # 莫亮金
    {"person_id": 6, "org_id": 5, "title": "静安区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 傅俊
    {"person_id": 7, "org_id": 2, "title": "静安区委常委、常务副区长，区政府党组副书记，区行政学院院长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 梅广清
    {"person_id": 8, "org_id": 2, "title": "静安区委常委、副区长，一级巡视员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 陈志忠
    {"person_id": 9, "org_id": 7, "title": "静安区委常委、区人民武装部政治委员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 萧烨璎
    {"person_id": 10, "org_id": 6, "title": "静安区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 龙婉丽
    {"person_id": 11, "org_id": 2, "title": "静安区副区长，区红十字会会长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "民盟成员，非中共党员"},
    # 姜坚
    {"person_id": 12, "org_id": 2, "title": "静安区副区长，市公安局静安分局局长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 张军
    {"person_id": 13, "org_id": 2, "title": "静安区副区长（援疆）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "上海市对口支援新疆工作前方指挥部（第十一批）副总指挥"},
    # 胡勇
    {"person_id": 14, "org_id": 2, "title": "静安区副区长", "start_date": "2025-04", "end_date": "present", "rank": "副厅级", "note": ""},
    # 施煜
    {"person_id": 15, "org_id": 2, "title": "静安区副区长", "start_date": "2025-11", "end_date": "present", "rank": "副厅级", "note": ""},
    # 顾云豪
    {"person_id": 16, "org_id": 8, "title": "静安区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 丁宝定
    {"person_id": 17, "org_id": 9, "title": "静安区政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 于勇
    {"person_id": 18, "org_id": 1, "title": "中共上海市静安区委书记（前任）", "start_date": "2021", "end_date": "2024-12", "rank": "正厅级", "note": "前任区委书记，后调任上海市人民政府副市长"},
    # 王华
    {"person_id": 19, "org_id": 2, "title": "静安区区长（前任）", "start_date": "2021", "end_date": "2024", "rank": "正厅级", "note": "前任区长，后调任徐汇区委副书记、区长"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────
relationships = [
    # 钟晓咏 — 翟磊 (搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档关系", "overlap_org": "上海市静安区", "overlap_period": "2024-12至今"},
    # 钟晓咏 — 于勇 (前后任)
    {"person_a": 1, "person_b": 18, "type": "前后任", "context": "钟晓咏接替于勇任静安区委书记", "overlap_org": "中共上海市静安区委员会", "overlap_period": "2024-12"},
    # 翟磊 — 王华 (前后任)
    {"person_a": 2, "person_b": 19, "type": "前后任", "context": "翟磊接替王华任静安区区长", "overlap_org": "上海市静安区人民政府", "overlap_period": "2024"},
    # 钟晓咏 — 王华 (前任搭档)
    {"person_a": 1, "person_b": 19, "type": "共事", "context": "钟晓咏任徐汇区长时的前任搭档王华接任其徐汇区长职位", "overlap_org": "上海市徐汇区人民政府", "overlap_period": "2023-2024"},
    # 钟晓咏 — 傅俊 (上下级)
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记—常务副区长", "overlap_org": "上海市静安区", "overlap_period": "2024-12至今"},
    # 翟磊 — 傅俊 (上下级)
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长—常务副区长", "overlap_org": "上海市静安区人民政府", "overlap_period": "2024至今"},
    # 钟晓咏 — 徐静 (上下级)
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委副书记", "overlap_org": "中共上海市静安区委员会", "overlap_period": "2024-12至今"},
    # 翟磊 — 徐静 (共事)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—区委副书记", "overlap_org": "上海市静安区", "overlap_period": ""},
    # 钟晓咏 — 各常委 (上下级)
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记—政法委书记", "overlap_org": "中共上海市静安区委员会", "overlap_period": "2024-12至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记—纪委书记", "overlap_org": "中共上海市静安区委员会", "overlap_period": "2024-12至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记—组织部部长", "overlap_org": "中共上海市静安区委员会", "overlap_period": "2024-12至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记—常委副区长", "overlap_org": "上海市静安区", "overlap_period": "2024-12至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记—人武部政委", "overlap_org": "中共上海市静安区委员会", "overlap_period": "2024-12至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "区委书记—宣传部部长", "overlap_org": "中共上海市静安区委员会", "overlap_period": "2024-12至今"},
]

# ── BUILD ──────────────────────────────────────────────────────────
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

if __name__ == "__main__":
    print(f"=== Building {SLUG} network ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Export person JSON files
    def write_person_json(person: dict, job_label: str):
        filename = f"{TODAY}-上海市-静安区-{job_label}-{person['name']}.json"
        output = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "上海市",
                "city": "静安区",
                "region": "静安区",
                "job": person["current_post"],
                "task_id": "shanghai_静安区",
                "time_focus": "2021-2026",
            },
            "identity": {
                "person_id": f"jingan_{person['name']}",
                "name": person["name"],
                "aliases": [],
                "gender": person.get("gender", ""),
                "ethnicity": person.get("ethnicity", ""),
                "birth": person.get("birth", ""),
                "birthplace": person.get("birthplace", ""),
                "native_place": person.get("birthplace", ""),
                "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": ["S001"]}],
                "party_join": person.get("party_join", ""),
                "work_start": person.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{person['name']}_{person.get('birth', '')}",
                    "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                    "official_profile_url": person.get("source", ""),
                },
            },
            "current_status": {
                "current_post": person["current_post"],
                "current_org": person["current_org"],
                "administrative_rank": "",
                "as_of": TODAY,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": pos.get("start_date", ""),
                    "end": pos.get("end_date", ""),
                    "org": pos["org_id"],
                    "title": pos["title"],
                    "rank": pos.get("rank", ""),
                    "notes": pos.get("note", ""),
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                }
                for pos in positions
                if pos["person_id"] == person["id"]
            ],
            "organizations": [
                {
                    "org_id": org["id"],
                    "name": org["name"],
                    "type": org["type"],
                    "level": org["level"],
                    "parent": org.get("parent", ""),
                    "location": org.get("location", ""),
                    "source_ids": ["S001"],
                }
                for org in organizations
                if org["id"] in {pos["org_id"] for pos in positions if pos["person_id"] == person["id"]}
            ],
            "relationships": [
                {
                    "person": p["name"],
                    "person_id": f"jingan_{p['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ("共事", "前后任") else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                }
                for r in relationships
                for p in persons
                if (r["person_a"] == person["id"] and r["person_b"] == p["id"]) or (r["person_b"] == person["id"] and r["person_a"] == p["id"])
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": [
                {
                    "id": "S001",
                    "title": "上海市静安区人民政府门户网站 - 领导之窗",
                    "url": "https://www.jingan.gov.cn/sy/004015/leadwindow.html",
                    "publisher": "上海市静安区人民政府",
                    "published_at": "",
                    "accessed_at": TODAY,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "Confirmed current officeholders from official leadership window",
                }
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "Detailed career timeline, birthplace, and education background details need further verification beyond official brief bios",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"完整简历：{person['name']}的详细教育背景、早期职业生涯、晋升时间线、籍贯",
                    "why_it_matters": "核心领导的履历完整度影响关系网络分析的深度",
                    "suggested_queries": [f"{person['name']} 简历 静安", f"{person['name']} 任前公示"],
                    "last_attempted": TODAY,
                }
            ],
        }
        path = os.path.join(PERSONS_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filename}")

    write_person_json(persons[0], "区委书记")  # 钟晓咏
    write_person_json(persons[1], "区长")  # 翟磊

    print(f"\n=== Done. Output in {STAGING_DIR} ===")
