#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
佛山市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Parent City:
Region: 佛山市
Targets: 市委书记 & 市长

Research Sources:
- 维基百科 (zh.wikipedia.org) — 佛山市词条、唐屹峰、郑轲、白涛
- 佛山市政府网站 (www.foshan.gov.cn)

Current status (as of 2026-07-22):
- 市委书记: 唐屹峰（2024年10月－，兼广东省副省长）
- 市长: 牟治平（2026年7月－）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "佛山市"
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
        "name": "唐屹峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年1月",
        "birthplace": "浙江温州",
        "native_place": "浙江温州",
        "education": "工程师（具体院校待查）",
        "party_join": "中共党员",
        "work_start": "待查（国家电网系统多年）",
        "current_post": "中共佛山市委书记、广东省副省长",
        "current_org": "中共佛山市委员会",
        "source": "Wikipedia:唐屹峰"
    },
    {
        "id": 2,
        "name": "牟治平",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1981年3月",
        "birthplace": "湖北恩施",
        "native_place": "湖北恩施",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共佛山市委副书记、市长",
        "current_org": "佛山市人民政府",
        "source": "Wikipedia:佛山市"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "胡钛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964年4月",
        "birthplace": "湖南双峰",
        "native_place": "湖南双峰",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "佛山市人大常委会主任",
        "current_org": "佛山市人民代表大会常务委员会",
        "source": "Wikipedia:佛山市"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "李政华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年4月",
        "birthplace": "广东兴宁",
        "native_place": "广东兴宁",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "佛山市政协主席",
        "current_org": "中国人民政治协商会议佛山市委员会",
        "source": "Wikipedia:佛山市"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "郑轲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年9月",
        "birthplace": "广东茂名",
        "native_place": "广东茂名",
        "education": "中山大学哲学学士",
        "party_join": "中共党员（1987年）",
        "work_start": "1989年6月",
        "current_post": "广东省政协副主席",
        "current_org": "中国人民政治协商会议广东省委员会",
        "source": "Wikipedia:郑轲"
    },
    {
        "id": 6,
        "name": "白涛",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1968年4月",
        "birthplace": "新疆伊犁",
        "native_place": "新疆伊犁",
        "education": "华南理工大学有机化工专业本科、管理科学与工程硕士",
        "party_join": "中共党员（1987年）",
        "work_start": "1990年6月",
        "current_post": "广东省委社会工作部副部长、省信访局局长",
        "current_org": "广东省信访局",
        "source": "Wikipedia:白涛(1968年)"
    },
    {
        "id": 7,
        "name": "郭文海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（2021年4月-10月任佛山市市长，后调任）",
        "current_org": "（已离任）",
        "source": "Wikipedia:佛山市"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共佛山市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "佛山市禅城区"
    },
    {
        "id": 2,
        "name": "佛山市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "佛山市禅城区"
    },
    {
        "id": 3,
        "name": "佛山市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "佛山市禅城区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议佛山市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议广东省委员会",
        "location": "佛山市禅城区"
    },
    {
        "id": 5,
        "name": "广东省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "广州市"
    },
    {
        "id": 6,
        "name": "中国人民政治协商会议广东省委员会",
        "type": "政协",
        "level": "省级",
        "parent": "",
        "location": "广州市"
    },
    {
        "id": 7,
        "name": "广东省信访局",
        "type": "政府",
        "level": "省级",
        "parent": "广东省人民政府",
        "location": "广州市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 唐屹峰
    {"person_id": 1, "org_id": 1, "title": "中共佛山市委书记", "start_date": "2024-10", "end_date": "present", "rank": "副部级（兼广东省副省长）", "note": "兼任广东省副省长（2025-10起）"},
    {"person_id": 1, "org_id": 5, "title": "广东省副省长", "start_date": "2025-10", "end_date": "present", "rank": "副部级", "note": "佛山市委书记兼任"},
    # 牟治平
    {"person_id": 2, "org_id": 2, "title": "佛山市市长", "start_date": "2026-07", "end_date": "present", "rank": "正厅级", "note": "上任时间来自Wikipedia"},
    {"person_id": 2, "org_id": 1, "title": "中共佛山市委副书记", "start_date": "2026-07", "end_date": "present", "rank": "正厅级", "note": "市委副书记兼市长"},
    # 胡钛
    {"person_id": 3, "org_id": 3, "title": "佛山市人大常委会主任", "start_date": "2021-11", "end_date": "present", "rank": "正厅级", "note": ""},
    # 李政华
    {"person_id": 4, "org_id": 4, "title": "佛山市政协主席", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": ""},
    # 郑轲（前任市委书记）
    {"person_id": 5, "org_id": 1, "title": "中共佛山市委书记", "start_date": "2021-06", "end_date": "2024-10", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "佛山市人大常委会主任", "start_date": "2021-06", "end_date": "2021-11", "rank": "正厅级", "note": "兼任人大主任"},
    {"person_id": 5, "org_id": 6, "title": "广东省政协副主席", "start_date": "2023-01", "end_date": "present", "rank": "副部级", "note": "2024年10月卸任佛山市委书记后继续担任省政协副主席"},
    # 白涛（前任市长）
    {"person_id": 6, "org_id": 2, "title": "佛山市市长", "start_date": "2021-10", "end_date": "2025-12", "rank": "正厅级", "note": "2021年10月任代市长，11月当选"},
    {"person_id": 6, "org_id": 1, "title": "中共佛山市委副书记", "start_date": "2021-10", "end_date": "2025-12", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "广东省信访局局长", "start_date": "2025-12", "end_date": "present", "rank": "正厅级", "note": "省委社会工作部副部长兼"},
    # 郭文海（前任市长）
    {"person_id": 7, "org_id": 2, "title": "佛山市市长", "start_date": "2021-04", "end_date": "2021-10", "rank": "正厅级", "note": "后调任他职"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记与市长是地级市最重要的党政搭档", "overlap_org": "中共佛山市委员会/佛山市人民政府", "overlap_period": "2026-07至今"},
    # 市委书记与前任市长
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "唐屹峰任市委书记时白涛任市长（2024-10至2025-12）", "overlap_org": "中共佛山市委员会/佛山市人民政府", "overlap_period": "2024-10至2025-12"},
    # 前后任市委书记
    {"person_a": 5, "person_b": 1, "type": "前后任", "context": "郑轲（2021-06至2024-10）→唐屹峰（2024-10至今）", "overlap_org": "中共佛山市委员会", "overlap_period": "2024-10交接"},
    # 前后任市长
    {"person_a": 7, "person_b": 6, "type": "前后任", "context": "郭文海（2021-04至2021-10）→白涛（2021-10至2025-12）", "overlap_org": "佛山市人民政府", "overlap_period": "2021-10交接"},
    {"person_a": 6, "person_b": 2, "type": "前后任", "context": "白涛（2021-10至2025-12）→牟治平（2026-07至今）", "overlap_org": "佛山市人民政府", "overlap_period": "2026-07交接"},
    # 市人大与市委
    {"person_a": 3, "person_b": 1, "type": "党政关系", "context": "市人大常委会主任与市委书记的党政协作", "overlap_org": "佛山市领导班子", "overlap_period": "2024-10至今"},
    # 市政协与市委
    {"person_a": 4, "person_b": 1, "type": "党政关系", "context": "市政协主席与市委书记的党政协作", "overlap_org": "佛山市领导班子", "overlap_period": "2024-10至今"},
    # 郑轲与白涛（前任党政搭档）
    {"person_a": 5, "person_b": 6, "type": "党政正职搭档", "context": "郑轲任市委书记时白涛任市长（2021-10至2024-10）", "overlap_org": "中共佛山市委员会/佛山市人民政府", "overlap_period": "2021-10至2024-10"},
    # 郑轲与郭文海（前任党政搭档）
    {"person_a": 5, "person_b": 7, "type": "党政正职搭档", "context": "郑轲任市委书记时郭文海任市长（2021-06至2021-10）", "overlap_org": "中共佛山市委员会/佛山市人民政府", "overlap_period": "2021-06至2021-10"},
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
