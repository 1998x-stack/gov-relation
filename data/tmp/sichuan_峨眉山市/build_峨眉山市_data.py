#!/usr/bin/env python3
"""峨眉山市 领导班子工作关系网络 — 数据构建脚本"""

import sqlite3
import sys
import os
from datetime import datetime

# Ensure gov_relation package is importable
BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build

SLUG = "峨眉山市"
DATE_TAG = datetime.now().strftime("%Y%m%d")

# Write to staging directory; promote with process_tmp.py
STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# ── Organizations ────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共峨眉山市委",
        "type": "党委",
        "level": "县级市",
        "parent": "中共乐山市委",
        "location": "四川省乐山市峨眉山市",
    },
    {
        "id": 2,
        "name": "峨眉山市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "乐山市人民政府",
        "location": "四川省乐山市峨眉山市",
    },
    {
        "id": 3,
        "name": "峨眉山市人大常委会",
        "type": "人大",
        "level": "县级市",
        "parent": "乐山市人大常委会",
        "location": "四川省乐山市峨眉山市",
    },
    {
        "id": 4,
        "name": "政协峨眉山市委员会",
        "type": "政协",
        "level": "县级市",
        "parent": "政协乐山市委员会",
        "location": "四川省乐山市峨眉山市",
    },
    {
        "id": 5,
        "name": "峨眉山市纪委监委",
        "type": "纪委",
        "level": "县级市",
        "parent": "中共峨眉山市委",
        "location": "四川省乐山市峨眉山市",
    },
    {
        "id": 6,
        "name": "峨眉山景区党工委",
        "type": "党委",
        "level": "县级",
        "parent": "中共乐山市委",
        "location": "四川省乐山市峨眉山市",
    },
    {
        "id": 7,
        "name": "峨眉山市公安局",
        "type": "政府",
        "level": "市级",
        "parent": "峨眉山市人民政府",
        "location": "四川省乐山市峨眉山市",
    },
]

# ── Persons ──────────────────────────────────────────────────────────────
PERSONS = [
    # 01 — 李良 (市委书记, 已离任)
    {
        "id": 1,
        "name": "李良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,  # 待查
        "birthplace": None,  # 待查
        "education": None,
        "party_join": None,
        "work_start": None,
        "current_post": "峨眉山市委书记（前任/已离任）",
        "current_org": "中共峨眉山市委",
        "source": "https://www.emeishan.gov.cn/emss/emyw/df2fa96992674174b53df5a40.html",
    },
    # 02 彭警 — 市长、市委副书记 (实际主持工作)
    {
        "id": 2,
        "name": "彭警",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "四川安岳",
        "education": "大学学历",
        "party_join": None,  # 待查
        "work_start": None,  # 待查
        "current_post": "峨眉山市委副书记、市人民政府市长",
        "current_org": "峨眉山市人民政府",
        "source": "https://www.emeishan.gov.cn/ems/zfld/index.html",
    },
    # 03 郑文武 — 市委副书记
    {
        "id": 3,
        "name": "郑文武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": None,
        "party_join": None,
        "work_start": None,
        "current_post": "峨眉山市委副书记",
        "current_org": "中共峨眉山市委",
        "source": "https://www.emeishan.gov.cn/ems/emyw/827881889095749.html",
    },
    # 04 何方 — 市人大常委会主任
    {
        "id": 4,
        "name": "何方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": None,
        "party_join": None,
        "work_start": None,
        "current_post": "峨眉山市人大常委会主任",
        "current_org": "峨眉山市人大常委会",
        "source": "https://www.emeishan.gov.cn/ems/emyw/827881889095749.html",
    },
    # 05 谭勇强 — 市政协主席
    {
        "id": 5,
        "name": "谭勇强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": None,
        "birthplace": None,
        "education": None,
        "party_join": None,
        "work_start": None,
        "current_post": "政协峨眉山市委员会主席",
        "current_org": "政协峨眉山市委员会",
        "source": "https://www.emeishan.gov.cn/ems/emyw/827881889095749.html",
    },
    # 06 曾明浩 — 市委常委、常务副市长
    {
        "id": 6,
        "name": "曾明浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年9月",
        "birthplace": "四川犍为",
        "education": "党校大学学历",
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "峨眉山市委常委、市政府常务副市长",
        "current_org": "峨眉山市人民政府",
        "source": "https://www.emeishan.gov.cn/ems/zfld/index.html",
    },
    # 07 范敏 — 市委常委、市政府党组成员、总工会主席
    {
        "id": 7,
        "name": "范敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "四川井研",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "峨眉山市委常委、市政府党组成员、市总工会主席",
        "current_org": "峨眉山市人民政府",
        "source": "https://www.emeishan.gov.cn/ems/zfld/index.html",
    },
    # 08 梁梦 — 市委常委、副市长（挂职）
    {
        "id": 8,
        "name": "梁梦",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988年3月",
        "birthplace": "四川成都",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "峨眉山市委常委、副市长（挂职）",
        "current_org": "峨眉山市人民政府",
        "source": "https://www.emeishan.gov.cn/ems/zfld/index.html",
    },
    # 09 胥楠 — 市委常委、副市长（挂职）
    {
        "id": 9,
        "name": "胥楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "四川南部",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "峨眉山市委常委、副市长（挂职）",
        "current_org": "峨眉山市人民政府",
        "source": "https://www.emeishan.gov.cn/ems/zfld/index.html",
    },
    # 10 李怡秋 — 副市长
    {
        "id": 10,
        "name": "李怡秋",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "四川乐山",
        "education": "在职大学毕业",
        "partner_join": None,  # 党外干部
        "work_start": None,
        "current_post": "峨眉山市人民政府副市长",
        "current_org": "峨眉山市人民政府",
        "source": "https://www.emeishan.gov.cn/ems/zfld/index.html",
    },
    # 11 任理军 — 副市长
    {
        "id": 11,
        "name": "任理军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "湖南岳阳",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "峨眉山市人民政府副市长",
        "current_org": "峨眉山市人民政府",
        "source": "https://www.emeishan.gov.cn/ems/zfld/index.html",
    },
    # 12 蔡其宏 — 副市长
    {
        "id": 12,
        "name": "蔡其宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年2月",
        "birthplace": "四川彭州",
        "education": "党校研究生毕业",
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "峨眉山市人民政府副市长",
        "current_org": "峨眉山市人民政府",
        "source": "https://www.emeishan.gov.cn/ems/zfld/index.html",
    },
    # 13 郭丁源 — 副市长、公安局局长
    {
        "id": 13,
        "name": "郭丁源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "四川乐山",
        "education": "在职大学毕业",
        "party_join": "中共党员",
        "work_start": None,
        "current_post": "峨眉山市人民政府副市长、公安局局长",
        "current_org": "峨眉山市公安局",
        "source": "https://www.emeishan.gov.cn/ems/zfld/index.html",
    },
]

# ── Positions ────────────────────────────────────────────────────────────
POSITIONS = [
    # 李良 (前书记)
    {"person_id": 1, "org_id": 1, "title": "峨眉山市委书记", "start": "2022?", "end": "2026-05?", "rank": "正县级",
     "note": "兼峨眉山景区党工委书记"},
    {"person_id": 1, "org_id": 6, "title": "峨眉山景区党工委书记", "start": "2022?", "end": "2026-05?", "rank": "正县级",
     "note": "兼任"},

    # 彭警 (市长)
    {"person_id": 2, "org_id": 1, "title": "峨眉山市委副书记", "start": None, "end": None, "rank": "正县级",
     "note": "2026年7月为实际主持工作的副书记"},
    {"person_id": 2, "org_id": 2, "title": "峨眉山市人民政府市长", "start": None, "end": None, "rank": "正县级",
     "note": "领导市政府全面工作"},

    # 郑文武
    {"person_id": 3, "org_id": 1, "title": "峨眉山市委副书记", "start": None, "end": None, "rank": "副县级",
     "note": "专职副书记"},

    # 何方
    {"person_id": 4, "org_id": 3, "title": "市人大常委会主任", "start": None, "end": None, "rank": "正县级"},

    # 谭勇强
    {"person_id": 5, "org_id": 4, "title": "市政协主席", "start": None, "end": None, "rank": "正县级"},

    # 曾明浩
    {"person_id": 6, "org_id": 1, "title": "峨眉山市委常委", "start": None, "end": None, "rank": "副县级"},
    {"person_id": 6, "org_id": 2, "title": "常务副市长", "start": None, "end": None, "rank": "副县级"},
    {"person_id": 6, "org_id": 2, "title": "市政府党组副书记", "start": None, "end": None, "rank": "副县级"},

    # 范敏
    {"person_id": 7, "org_id": 1, "title": "峨眉山市委常委", "start": None, "end": None, "rank": "副县级"},
    {"person_id": 7, "org_id": 2, "title": "市政府党组成员", "start": None, "end": None, "rank": "副县级"},
    {"person_id": 7, "org_id": 2, "title": "市总工会主席", "start": None, "end": None, "rank": "副县级"},

    # 梁梦 (挂职)
    {"person_id": 8, "org_id": 1, "title": "峨眉山市委常委（挂职）", "start": None, "end": None, "rank": "挂职"},
    {"person_id": 8, "org_id": 2, "title": "副市长（挂职）", "start": None, "end": None, "rank": "挂职"},

    # 胥楠 (挂职)
    {"person_id": 9, "org_id": 1, "title": "峨眉山市委常委（挂职）", "start": None, "end": None, "rank": "挂职"},
    {"person_id": 9, "org_id": 2, "title": "副市长（挂职）", "start": None, "end": None, "rank": "挂职"},

    # 李怡秋
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": None, "end": None, "rank": "副县级"},

    # 任理军
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": None, "end": None, "rank": "副县级"},

    # 蔡其宏
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": None, "end": None, "rank": "副县级"},

    # 郭丁源
    {"person_id": 13, "org_id": 7, "title": "副市长、公安局局长", "start": None, "end": None, "rank": "副县级"},
]

# ── Relationships ────────────────────────────────────────────────────────
RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "李良（书记）与彭警（市长）搭班子",
     "overlap_org": "中共峨眉山市委/市政府", "overlap_period": "至2026年李良离任"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "书记+专职副书记",
     "overlap_org": "中共峨眉山市委", "overlap_period": "李良在任期间"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "书记+常务副市长",
     "overlap_org": "中共峨眉山市委", "overlap_period": "李良在任期间"},
    {"person_a": 2, "person_b": 3, "type": "党政搭档", "context": "市长（主持工作）+ 专职副书记",
     "overlap_org": "中共峨眉山市委", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "市长+常务副市长",
     "overlap_org": "峨眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 4, "type": "同级协作", "context": "市长+人大主任",
     "overlap_org": "峨眉山市", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 5, "type": "同级协作", "context": "市长+政协主席",
     "overlap_org": "峨眉山市", "overlap_period": "现任"},
    {"person_a": 6, "person_b": 7, "type": "常委同事", "context": "同届市委常委",
     "overlap_org": "中共峨眉山市委", "overlap_period": "现任"},
    {"person_a": 6, "person_b": 8, "type": "常委同事", "context": "同届市委常委、常务+挂职副市长",
     "overlap_org": "中共峨眉山市委", "overlap_period": "现任"},
    {"person_a": 6, "person_b": 9, "type": "常委同事", "context": "同届市委常委、常务+挂职副市长",
     "overlap_org": "中共峨眉山市委", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "市长+副市长",
     "overlap_org": "峨眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "市长+副市长",
     "overlap_org": "峨眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "市长+副市长",
     "overlap_org": "峨眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "市长+副市长/公安局局长",
     "overlap_org": "峨眉山市人民政府", "overlap_period": "现任"},
]

# ── Entry Point ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"Build complete: {SLUG}")