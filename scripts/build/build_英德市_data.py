#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英德市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 清远市
Region: 英德市
Targets: 市委书记 & 市长

Research Sources:
- 英德市人民政府网 — 领导之窗 (www.yingde.gov.cn)
  - 市委: zwgk/zzjg/ldzc/zggcdydswyh/
  - 市政府: zwgk/zzjg/ldzc/ydsrmzf/

Current status (as of 2026-07-22):
- 市委书记: 陈龙兴（2025年9月－）
- 市长: 翟永鸣

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "英德市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "陈龙兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "法学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "英德市委书记、一级调研员",
        "current_org": "中共英德市委员会",
        "source": "英德市人民政府网: 领导之窗-陈龙兴; 英德市人民政府网: 政务要闻-履新首次调研(2025-09-28)"
    },
    {
        "id": 2,
        "name": "翟永鸣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "英德市委副书记、市政府党组书记、市长",
        "current_org": "英德市人民政府",
        "source": "英德市人民政府网: 领导之窗-翟永鸣"
    },
    # ════════════════════════════════════════
    # 市委常委（副职领导）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "黄江波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委（待确认具体职务）",
        "current_org": "中共英德市委员会",
        "source": "英德市人民政府网: 领导之窗-中国共产党英德市委员会"
    },
    {
        "id": 4,
        "name": "张贻强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委（待确认具体职务）",
        "current_org": "中共英德市委员会",
        "source": "英德市人民政府网: 领导之窗; 英德政务要闻(2025-09-28市领导参加调研)"
    },
    {
        "id": 5,
        "name": "岳锐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委（待确认具体职务）",
        "current_org": "中共英德市委员会",
        "source": "英德市人民政府网: 领导之窗-中国共产党英德市委员会"
    },
    {
        "id": 6,
        "name": "蔡创",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委（待确认具体职务）",
        "current_org": "中共英德市委员会",
        "source": "英德市人民政府网: 领导之窗-中国共产党英德市委员会"
    },
    {
        "id": 7,
        "name": "廖永坚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委（待确认具体职务）",
        "current_org": "中共英德市委员会",
        "source": "英德市人民政府网: 领导之窗-中国共产党英德市委员会"
    },
    {
        "id": 8,
        "name": "罗伟权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共英德市委员会/英德市人民政府",
        "source": "英德市人民政府网: 领导之窗-中国共产党英德市委员会/英德市人民政府"
    },
    {
        "id": 9,
        "name": "李韶锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委（待确认具体职务）",
        "current_org": "中共英德市委员会",
        "source": "英德市人民政府网: 领导之窗-中国共产党英德市委员会"
    },
    {
        "id": 10,
        "name": "何靓",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委（待确认具体职务）",
        "current_org": "中共英德市委员会",
        "source": "英德市人民政府网: 领导之窗-中国共产党英德市委员会"
    },
    {
        "id": 11,
        "name": "蔡伟新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、市政府党组副书记、副市长",
        "current_org": "中共英德市委员会/英德市人民政府",
        "source": "英德市人民政府网: 领导之窗-蔡伟新"
    },
    # ════════════════════════════════════════
    # 其他副市长
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "周妍",
        "gender": "女",
        "ethnicity": "瑶族",
        "birth": "1981年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "",
        "work_start": "待查",
        "current_post": "英德市人民政府副市长",
        "current_org": "英德市人民政府",
        "source": "英德市人民政府网: 领导之窗-周妍"
    },
    {
        "id": 13,
        "name": "何海华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "英德市人民政府副市长",
        "current_org": "英德市人民政府",
        "source": "英德市人民政府网: 领导之窗-英德市人民政府"
    },
    {
        "id": 14,
        "name": "罗亚生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "英德市人民政府副市长",
        "current_org": "英德市人民政府",
        "source": "英德市人民政府网: 领导之窗-英德市人民政府"
    },
    {
        "id": 15,
        "name": "郑远锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "英德市人民政府副市长",
        "current_org": "英德市人民政府",
        "source": "英德市人民政府网: 领导之窗-英德市人民政府"
    },
    {
        "id": 16,
        "name": "梁毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "英德市人民政府副市长",
        "current_org": "英德市人民政府",
        "source": "英德市人民政府网: 领导之窗-英德市人民政府"
    },
    {
        "id": 17,
        "name": "廖晓明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "英德市人民政府副市长",
        "current_org": "英德市人民政府",
        "source": "英德市人民政府网: 领导之窗-英德市人民政府"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共英德市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共清远市委员会",
        "location": "英德市"
    },
    {
        "id": 2,
        "name": "英德市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "清远市人民政府",
        "location": "英德市"
    },
    {
        "id": 3,
        "name": "英德市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级市",
        "parent": "清远市人民代表大会常务委员会",
        "location": "英德市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议英德市委员会",
        "type": "政协",
        "level": "县级市",
        "parent": "中国人民政治协商会议清远市委员会",
        "location": "英德市"
    },
    {
        "id": 5,
        "name": "中共清远市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "清远市"
    },
    {
        "id": 6,
        "name": "清远市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "清远市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 陈龙兴（现任市委书记）
    {"person_id": 1, "org_id": 1, "title": "英德市委书记", "start": "2025-09", "end": "present", "rank": "正处级", "note": "一级调研员；2025年9月履新，首次调研重走习近平总书记视察英德路线"},
    # 陈龙兴曾任职务(待查)
    # 翟永鸣（现任市长）
    {"person_id": 2, "org_id": 2, "title": "英德市市长", "start": "", "end": "present", "rank": "正处级", "note": "市政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "英德市委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 市委常委（共性）
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "市政府党组副书记、副市长", "start": "", "end": "present", "rank": "副处级", "note": "常务副市长"},
    # 其他副市长
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "分管教育、卫健等"},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记陈龙兴与市长翟永鸣是英德市最重要的党政搭档", "overlap_org": "中共英德市委员会/英德市人民政府", "overlap_period": "2025-09至今"},
    # 市委班子核心成员
    {"person_a": 1, "person_b": 3, "type": "上下级关系", "context": "陈龙兴与黄江波为市委班子上下级", "overlap_org": "中共英德市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级关系", "context": "陈龙兴与张贻强为市委班子上下级；张贻强陪同陈龙兴履新首次调研", "overlap_org": "中共英德市委员会", "overlap_period": "2025-09至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级关系", "context": "陈龙兴与蔡伟新（常务副市长）为党政班子上下级", "overlap_org": "中共英德市委员会/英德市人民政府", "overlap_period": "至今"},
    # 党政班子交叉关系
    {"person_a": 2, "person_b": 11, "type": "上下级关系", "context": "翟永鸣与蔡伟新为市政府正副职", "overlap_org": "英德市人民政府", "overlap_period": "至今"},
]

# ── Build ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")
