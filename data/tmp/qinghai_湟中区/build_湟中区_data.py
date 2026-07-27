#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 湟中区 (Huangzhong District), 西宁市, 青海省."""

import sys
import os
import sqlite3
from datetime import datetime

# Add repo root to path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, BASE)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TASK_ID = "qinghai_湟中区"
TMP = os.path.join(BASE, "data/tmp", TASK_ID)
DB_PATH = os.path.join(TMP, "湟中区_network.db")
GEXF_PATH = os.path.join(TMP, "湟中区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "韩俊良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西宁市湟中区委书记",
        "current_org": "中共西宁市湟中区委员会",
        "source": "http://www.huangzhong.gov.cn/html/dzdt/10366.html"
    },
    {
        "id": 2,
        "name": "孟高冰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西宁市湟中区区长",
        "current_org": "西宁市湟中区人民政府",
        "source": "http://www.huangzhong.gov.cn/html/qzfld/10229.html"
    },

    # ── Deputy District Chiefs (副区长) ──
    {
        "id": 3,
        "name": "华巍",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟中区副区长",
        "current_org": "西宁市湟中区人民政府",
        "source": "http://www.huangzhong.gov.cn/html/qzfld/9817.html"
    },
    {
        "id": 4,
        "name": "彭峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟中区副区长（常务）",
        "current_org": "西宁市湟中区人民政府",
        "source": "http://www.huangzhong.gov.cn/html/qzfld/7495.html"
    },
    {
        "id": 5,
        "name": "张海杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟中区副区长",
        "current_org": "西宁市湟中区人民政府",
        "source": "http://www.huangzhong.gov.cn/html/qzfld/7493.html"
    },
    {
        "id": 6,
        "name": "王静茹",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟中区副区长",
        "current_org": "西宁市湟中区人民政府",
        "source": "http://www.huangzhong.gov.cn/html/qzfld/9302.html"
    },
    {
        "id": 7,
        "name": "商志刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟中区副区长",
        "current_org": "西宁市湟中区人民政府",
        "source": "http://www.huangzhong.gov.cn/html/qzfld/7489.html"
    },
    {
        "id": 8,
        "name": "王振华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟中区副区长",
        "current_org": "西宁市湟中区人民政府",
        "source": "http://www.huangzhong.gov.cn/html/qzfld/10152.html"
    },

    # ── Predecessor Leaders ──
    {
        "id": 9,
        "name": "郭健",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原湟中区区长）",
        "current_org": "",
        "source": "http://www.huangzhong.gov.cn/html/dzdt/8829.html"
    },
    {
        "id": 10,
        "name": "吉辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原湟中区委书记）",
        "current_org": "",
        "source": "http://www.huangzhong.gov.cn/html/dzdt/5656.html"
    },
    {
        "id": 11,
        "name": "李晓舸",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原湟中区委书记）",
        "current_org": "",
        "source": "http://www.huangzhong.gov.cn/html/tpxw/1323.html"
    },
]

organizations = [
    {"id": 1, "name": "中共西宁市湟中区委员会", "type": "党委",
     "level": "县处级", "parent": "中共西宁市委", "location": "青海省西宁市湟中区"},
    {"id": 2, "name": "西宁市湟中区人民政府", "type": "政府",
     "level": "县处级", "parent": "西宁市人民政府", "location": "青海省西宁市湟中区"},
    {"id": 3, "name": "西宁市湟中区人大常委会", "type": "人大",
     "level": "县处级", "parent": "", "location": "青海省西宁市湟中区"},
    {"id": 4, "name": "政协西宁市湟中区委员会", "type": "政协",
     "level": "县处级", "parent": "", "location": "青海省西宁市湟中区"},
    {"id": 5, "name": "中共西宁市湟中区纪律检查委员会", "type": "党委",
     "level": "县处级", "parent": "中共西宁市湟中区委员会", "location": "青海省西宁市湟中区"},
    {"id": 6, "name": "多巴新城建设管理委员会", "type": "事业单位",
     "level": "县处级", "parent": "", "location": "青海省西宁市湟中区多巴镇"},
]

positions = [
    # 韩俊良
    {"person_id": 1, "org_id": 1, "title": "西宁市湟中区委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "2022年湟中区第三次党代会当选区委书记，仍在任（截至2026年7月）"},
    # 孟高冰
    {"person_id": 2, "org_id": 2, "title": "西宁市湟中区区长",
     "start_date": "2026-01", "end_date": "present", "rank": "县处级正职",
     "note": "原代理区长，2026年1月区二届人大六次会议当选区长"},
    {"person_id": 2, "org_id": 2, "title": "湟中区副区长（代理区长）",
     "start_date": "", "end_date": "2026-01", "rank": "县处级副职",
     "note": "任副区长、代理区长，主持区政府工作"},
    # 副区长
    {"person_id": 3, "org_id": 2, "title": "湟中区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责发改、工信、商务、文旅、财政税收、金融等方面工作"},
    {"person_id": 4, "org_id": 2, "title": "湟中区副区长（常务）",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责区政府常务工作"},
    {"person_id": 5, "org_id": 2, "title": "湟中区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责公安、国家安全、司法、信访等方面工作"},
    {"person_id": 6, "org_id": 2, "title": "湟中区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 7, "org_id": 2, "title": "湟中区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责农业农村、乡村振兴、交通、退役军人事务、供销等方面工作"},
    {"person_id": 8, "org_id": 2, "title": "湟中区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责民政、交通运输、生态环境、城乡管理等方面工作"},
    # 前任
    {"person_id": 9, "org_id": 2, "title": "湟中区区长",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "前任区长，2024年度抓基层党建工作述职评议会仍以区长身份出席"},
    {"person_id": 10, "org_id": 1, "title": "湟中区委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "前任区委书记，2022年主持全区科级干部研讨班"},
    {"person_id": 11, "org_id": 1, "title": "湟中区委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "前任区委书记，2021年调研司法行政队伍教育整顿工作"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "现任区委书记与区长，同一届班子主要领导搭档",
     "overlap_org": "中共西宁市湟中区委员会/西宁市湟中区人民政府",
     "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor",
     "context": "韩俊良接替吉辉任湟中区委书记",
     "overlap_org": "中共西宁市湟中区委员会",
     "overlap_period": ""},
    {"person_a": 10, "person_b": 11, "type": "predecessor_successor",
     "context": "吉辉接替李晓舸任湟中区委书记",
     "overlap_org": "中共西宁市湟中区委员会",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "predecessor_successor",
     "context": "孟高冰接替郭健任湟中区区长",
     "overlap_org": "西宁市湟中区人民政府",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "韩俊良任区委书记期间，郭健曾任区长，后孟高冰接任",
     "overlap_org": "中共西宁市湟中区委员会/西宁市湟中区人民政府",
     "overlap_period": "~2024-2025"},
]

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(TMP, exist_ok=True)
    run_build(
        slug="湟中区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
