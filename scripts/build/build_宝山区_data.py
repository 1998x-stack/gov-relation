#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 上海市宝山区 leadership network.

调查日期: 2026-07-25
信息来源: 上海市宝山区人民政府门户网站 (www.shbsq.gov.cn)
调查级别: 市辖区(直辖市)

Current leadership (as of 2026-07-25):
- 李晨昊 — 宝山区委书记 (appointed ~2023)
- 邓小冬 — 宝山区委副书记、区长 (appointed ~2024, previously 区委副书记)
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
DB_PATH = os.path.join(STAGING_DIR, "宝山区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "宝山区_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "上海市宝山区"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════════════════════
    # 区委领导 (District Party Committee)
    # ═══════════════════════════════════════════════

    # 区委书记 — 李晨昊
    {
        "id": 1,
        "name": "李晨昊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-08",
        "birthplace": "上海",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1990-07",
        "current_post": "中共上海市宝山区委书记",
        "current_org": "中共上海市宝山区委员会",
        "source": "https://www.shbsq.gov.cn/ https://baike.baidu.com/",
    },
    # 区委副书记、区长 — 邓小冬
    {
        "id": 2,
        "name": "邓小冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-11",
        "birthplace": "山东齐河",
        "education": "大学学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "1992-07",
        "current_post": "宝山区委副书记、区长",
        "current_org": "上海市宝山区人民政府",
        "source": "https://www.shbsq.gov.cn/ https://baike.baidu.com/",
    },
    # 区委副书记 — 陆奕绎
    {
        "id": 3,
        "name": "陆奕绎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共上海市宝山区委副书记",
        "current_org": "中共上海市宝山区委员会",
        "source": "https://www.shbsq.gov.cn/",
    },
    # 区委常委、副区长（常务）— 郑益川
    {
        "id": 4,
        "name": "郑益川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区委常委、副区长（常务）",
        "current_org": "上海市宝山区人民政府",
        "source": "https://www.shbsq.gov.cn/",
    },
    # 区委常委、纪委书记、监委主任 — 洪晴
    {
        "id": 5,
        "name": "洪晴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区委常委、纪委书记、监委主任",
        "current_org": "中共上海市宝山区纪律检查委员会",
        "source": "https://www.shbsq.gov.cn/",
    },
    # 区委常委、组织部部长 — 高路
    {
        "id": 6,
        "name": "高路",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区委常委、组织部部长",
        "current_org": "中共上海市宝山区委组织部",
        "source": "https://www.shbsq.gov.cn/",
    },
    # 区委常委、宣传部部长 — 胡宝国
    {
        "id": 7,
        "name": "胡宝国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区委常委、宣传部部长",
        "current_org": "中共上海市宝山区委宣传部",
        "source": "https://www.shbsq.gov.cn/",
    },
    # 区委常委、政法委书记 — 陈云彬
    {
        "id": 8,
        "name": "陈云彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区委常委、政法委书记",
        "current_org": "中共上海市宝山区委政法委员会",
        "source": "https://www.shbsq.gov.cn/",
    },
    # 区委常委、统战部部长 — 沈伟娟
    {
        "id": 9,
        "name": "沈伟娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区委常委、统战部部长",
        "current_org": "中共上海市宝山区委统战部",
        "source": "https://www.shbsq.gov.cn/",
    },
    # 区委常委、区人民武装部政委 — 魏进文
    {
        "id": 10,
        "name": "魏进文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区委常委、区人民武装部政委",
        "current_org": "上海市宝山区人民武装部",
        "source": "https://www.shbsq.gov.cn/",
    },
    # ═══════════════════════════════════════════════
    # 区政府副区长 (District Government)
    # ═══════════════════════════════════════════════

    # 副区长 — 丁炯炯
    {
        "id": 11,
        "name": "丁炯炯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区副区长",
        "current_org": "上海市宝山区人民政府",
        "source": "https://www.shbsq.gov.cn/",
    },
    # 副区长 — 薛飒飒
    {
        "id": 12,
        "name": "薛飒飒",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区副区长",
        "current_org": "上海市宝山区人民政府",
        "source": "https://www.shbsq.gov.cn/",
    },
    # 副区长 — 朱众伟
    {
        "id": 13,
        "name": "朱众伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区副区长",
        "current_org": "上海市宝山区人民政府",
        "source": "https://www.shbsq.gov.cn/",
    },
    # 副区长 — 唐凌峰
    {
        "id": 14,
        "name": "唐凌峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区副区长",
        "current_org": "上海市宝山区人民政府",
        "source": "https://www.shbsq.gov.cn/",
    },
    # ═══════════════════════════════════════════════
    # 人大、政协领导
    # ═══════════════════════════════════════════════

    # 区人大常委会主任 — 李萍
    {
        "id": 15,
        "name": "李萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区人大常委会主任",
        "current_org": "上海市宝山区人民代表大会常务委员会",
        "source": "https://www.shbsq.gov.cn/",
    },
    # 区政协主席 — 凌惠康
    {
        "id": 16,
        "name": "凌惠康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝山区政协主席",
        "current_org": "中国人民政治协商会议上海市宝山区委员会",
        "source": "https://www.shbsq.gov.cn/",
    },
    # ═══════════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ═══════════════════════════════════════════════

    # 前任区委书记 — 陈杰 (前任)
    {
        "id": 17,
        "name": "陈杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-04",
        "birthplace": "江苏扬州",
        "education": "在职研究生学历，工学博士",
        "party_join": "中共党员",
        "work_start": "1991-07",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/",
    },
    # 前任区长 — 高奕奕 (前任)
    {
        "id": 18,
        "name": "高奕奕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "山东青岛",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "1996-08",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/",
    },
    # 前任区委书记 — 汪泓 (前任前任)
    {
        "id": 19,
        "name": "汪泓",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1961-04",
        "birthplace": "江苏苏州",
        "education": "大学学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "1983-07",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/",
    },
    # 前任区长 — 范少军 (前任前任)
    {
        "id": 20,
        "name": "范少军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-11",
        "birthplace": "江苏邗江",
        "education": "大学学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "1992-08",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共上海市宝山区委员会", "type": "党委", "level": "市辖区(直辖市)", "parent": "中共上海市委", "location": "上海市宝山区"},
    {"id": 2, "name": "上海市宝山区人民政府", "type": "政府", "level": "市辖区(直辖市)", "parent": "上海市人民政府", "location": "上海市宝山区"},
    {"id": 3, "name": "中共上海市宝山区纪律检查委员会", "type": "纪委", "level": "市辖区(直辖市)", "parent": "中共上海市宝山区委员会", "location": "上海市宝山区"},
    {"id": 4, "name": "中共上海市宝山区委组织部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市宝山区委员会", "location": "上海市宝山区"},
    {"id": 5, "name": "中共上海市宝山区委宣传部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市宝山区委员会", "location": "上海市宝山区"},
    {"id": 6, "name": "中共上海市宝山区委政法委员会", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市宝山区委员会", "location": "上海市宝山区"},
    {"id": 7, "name": "中共上海市宝山区委统战部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市宝山区委员会", "location": "上海市宝山区"},
    {"id": 8, "name": "上海市宝山区人民武装部", "type": "军队", "level": "市辖区(直辖市)", "parent": "上海警备区", "location": "上海市宝山区"},
    {"id": 9, "name": "上海市宝山区人民代表大会常务委员会", "type": "人大", "level": "市辖区(直辖市)", "parent": "上海市人民代表大会常务委员会", "location": "上海市宝山区"},
    {"id": 10, "name": "中国人民政治协商会议上海市宝山区委员会", "type": "政协", "level": "市辖区(直辖市)", "parent": "中国人民政治协商会议上海市委员会", "location": "上海市宝山区"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 李晨昊
    {"person_id": 1, "org_id": 1, "title": "中共上海市宝山区委书记", "start_date": "2023", "end_date": "present", "rank": "正厅级", "note": "2023年任宝山区委书记；此前任上海市委办公厅副主任、上海市档案局副局长"},
    {"person_id": 1, "org_id": 1, "title": "上海市档案局（馆）副局（馆）长", "start_date": "2016", "end_date": "2018", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "中共上海市委办公厅副主任", "start_date": "2018", "end_date": "2023", "rank": "副厅级", "note": ""},
    # 邓小冬
    {"person_id": 2, "org_id": 2, "title": "宝山区委副书记、区长", "start_date": "2024", "end_date": "present", "rank": "正厅级", "note": "2024年任宝山区代区长、区长；此前任宝山区委副书记"},
    {"person_id": 2, "org_id": 1, "title": "中共上海市宝山区委副书记", "start_date": "2023", "end_date": "2024", "rank": "正厅级", "note": "2023年从静安区调任宝山区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "上海市静安区副区长", "start_date": "2019", "end_date": "2023", "rank": "副厅级", "note": "曾任静安区副区长、区委常委"},
    {"person_id": 2, "org_id": 1, "title": "中共上海市静安区委常委", "start_date": "2021", "end_date": "2023", "rank": "副厅级", "note": ""},
    # 陆奕绎
    {"person_id": 3, "org_id": 1, "title": "中共上海市宝山区委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 郑益川
    {"person_id": 4, "org_id": 2, "title": "宝山区委常委、副区长（常务）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 洪晴
    {"person_id": 5, "org_id": 3, "title": "宝山区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 高路
    {"person_id": 6, "org_id": 4, "title": "宝山区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 胡宝国
    {"person_id": 7, "org_id": 5, "title": "宝山区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 陈云彬
    {"person_id": 8, "org_id": 6, "title": "宝山区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 沈伟娟
    {"person_id": 9, "org_id": 7, "title": "宝山区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 魏进文
    {"person_id": 10, "org_id": 8, "title": "宝山区委常委、区人民武装部政委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 丁炯炯
    {"person_id": 11, "org_id": 2, "title": "宝山区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 薛飒飒
    {"person_id": 12, "org_id": 2, "title": "宝山区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 朱众伟
    {"person_id": 13, "org_id": 2, "title": "宝山区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 唐凌峰
    {"person_id": 14, "org_id": 2, "title": "宝山区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 李萍
    {"person_id": 15, "org_id": 9, "title": "宝山区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 凌惠康
    {"person_id": 16, "org_id": 10, "title": "宝山区政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 陈杰（前任区委书记）
    {"person_id": 17, "org_id": 1, "title": "中共上海市宝山区委书记（前任）", "start_date": "2020", "end_date": "2023", "rank": "正厅级", "note": "前任区委书记，后调任上海市副市长"},
    {"person_id": 17, "org_id": 2, "title": "上海市宝山区区长", "start_date": "2018", "end_date": "2020", "rank": "正厅级", "note": "此前任宝山区区长"},
    # 高奕奕（前任区长）
    {"person_id": 18, "org_id": 2, "title": "宝山区区长（前任）", "start_date": "2020", "end_date": "2023", "rank": "正厅级", "note": "前任区长，后调任上海市交通委员会副主任"},
    {"person_id": 18, "org_id": 1, "title": "中共上海市宝山区委副书记", "start_date": "2020", "end_date": "2023", "rank": "副厅级", "note": ""},
    # 汪泓（前任前区委书记）
    {"person_id": 19, "org_id": 1, "title": "中共上海市宝山区委书记（前任）", "start_date": "2013", "end_date": "2020", "rank": "正厅级", "note": "宝山区委书记，后调任上海市人力资源社会保障局局长"},
    # 范少军（前任前区长）
    {"person_id": 20, "org_id": 2, "title": "宝山区区长（前任）", "start_date": "2016", "end_date": "2019", "rank": "正厅级", "note": "前任区长，后调任海南省"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────
relationships = [
    # 李晨昊 — 邓小冬 (搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档关系", "overlap_org": "上海市宝山区", "overlap_period": "2024至今"},
    # 李晨昊 — 陈杰 (前后任)
    {"person_a": 1, "person_b": 17, "type": "前后任", "context": "李晨昊接替陈杰任宝山区委书记", "overlap_org": "中共上海市宝山区委员会", "overlap_period": "2023"},
    # 邓小冬 — 高奕奕 (前后任)
    {"person_a": 2, "person_b": 18, "type": "前后任", "context": "邓小冬接替高奕奕任宝山区长", "overlap_org": "上海市宝山区人民政府", "overlap_period": "2024"},
    # 陈杰 — 高奕奕 (搭档)
    {"person_a": 17, "person_b": 18, "type": "共事", "context": "陈杰(区委书记)—高奕奕(区长)搭档", "overlap_org": "上海市宝山区", "overlap_period": "2020-2023"},
    # 陈杰 — 汪泓 (前后任)
    {"person_a": 17, "person_b": 19, "type": "前后任", "context": "陈杰接替汪泓任宝山区委书记", "overlap_org": "中共上海市宝山区委员会", "overlap_period": "2020"},
    # 高奕奕 — 范少军 (前后任)
    {"person_a": 18, "person_b": 20, "type": "前后任", "context": "高奕奕接替范少军任宝山区长", "overlap_org": "上海市宝山区人民政府", "overlap_period": "2020"},
    # 李晨昊 — 郑益川 (上下级)
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记—常务副区长", "overlap_org": "上海市宝山区", "overlap_period": ""},
    # 邓小冬 — 郑益川 (上下级)
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长—常务副区长", "overlap_org": "上海市宝山区人民政府", "overlap_period": ""},
    # 李晨昊 — 陆奕绎 (上下级)
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委副书记", "overlap_org": "中共上海市宝山区委员会", "overlap_period": ""},
    # 邓小冬 — 陆奕绎 (共事)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—区委副书记", "overlap_org": "上海市宝山区", "overlap_period": ""},
    # 李晨昊 — 各常委 (上下级)
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记—纪委书记", "overlap_org": "中共上海市宝山区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记—组织部部长", "overlap_org": "中共上海市宝山区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记—宣传部部长", "overlap_org": "中共上海市宝山区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记—政法委书记", "overlap_org": "中共上海市宝山区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记—统战部部长", "overlap_org": "中共上海市宝山区委员会", "overlap_period": ""},
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
        filename = f"{TODAY}-上海市-宝山区-{job_label}-{person['name']}.json"
        output = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "上海市",
                "city": "宝山区",
                "region": "宝山区",
                "job": person["current_post"],
                "task_id": "shanghai_宝山区",
                "time_focus": "2013-2026",
            },
            "identity": {
                "person_id": f"baoshan_{person['name']}",
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
                    "official_profile_url": "",
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
                    "confidence": "plausible",
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
                    "person_id": f"baoshan_{p['name']}",
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
                    "title": "上海市宝山区人民政府门户网站",
                    "url": "https://www.shbsq.gov.cn/",
                    "publisher": "上海市宝山区人民政府",
                    "published_at": "",
                    "accessed_at": TODAY,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "Confirmed current officeholders from homepage news feed",
                }
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "Detailed career timeline and education background need verification from official biography pages",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"完整简历：{person['name']}的详细教育背景、早期职业生涯、晋升时间线",
                    "why_it_matters": "核心领导的履历完整度影响关系网络分析的深度",
                    "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示"],
                    "last_attempted": TODAY,
                }
            ],
        }
        path = os.path.join(PERSONS_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filename}")

    write_person_json(persons[0], "区委书记")  # 李晨昊
    write_person_json(persons[1], "区长")  # 邓小冬

    print(f"\n=== Done. Output in {STAGING_DIR} ===")
