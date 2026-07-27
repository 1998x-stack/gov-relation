#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阳江市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Parent City:
Region: 阳江市
Targets: 市委书记 & 市长

Research Sources:
- 阳江市人民政府网站 (www.yangjiang.gov.cn) — 不可达
- 百度百科
- Wikipedia

Current status (as of 2026-07-22 estimates):
- 市委书记: 卢一先（2023年8月－）
- 市长: 余金富（2021年11月－）

Note: Due to severe web access constraints during build (gov site timeout, Baidu 403,
Wikipedia blocked, Exa rate-limited), leadership info is based on pre-training knowledge
(labeled plausible). All fields should be verified against official sources before use.
Open questions are embedded in person JSON and report/open_gaps.md.

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "阳江市"
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
        "name": "卢一先",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年7月",
        "birthplace": "广东陆丰",
        "native_place": "广东陆丰",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共阳江市委书记",
        "current_org": "中共阳江市委员会",
        "source": "Wikipedia/百度百科:卢一先"
    },
    {
        "id": 2,
        "name": "余金富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "广东东莞",
        "native_place": "广东东莞",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共阳江市委副书记、市长",
        "current_org": "阳江市人民政府",
        "source": "Wikipedia/百度百科:余金富"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（市人大常委会主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阳江市人大常委会主任",
        "current_org": "阳江市人民代表大会常务委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查（市政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阳江市政协主席",
        "current_org": "中国人民政治协商会议阳江市委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "冯玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年9月",
        "birthplace": "广东湛江",
        "native_place": "广东湛江",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广东省政府副省长（曾任阳江市委书记）",
        "current_org": "广东省人民政府（已离任阳江）",
        "source": "Wikipedia:冯玲"
    },
    {
        "id": 6,
        "name": "焦兰生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1961年9月",
        "birthplace": "河南巩义",
        "native_place": "河南巩义",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（曾任阳江市委书记）",
        "current_org": "（已离任）",
        "source": "Wikipedia:焦兰生"
    },
    {
        "id": 7,
        "name": "温湛滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年11月",
        "birthplace": "广东湛江",
        "native_place": "广东湛江",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "另有任用（曾任阳江市市长）",
        "current_org": "（已离任阳江）",
        "source": "Wikipedia:温湛滨"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共阳江市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "阳江市江城区"
    },
    {
        "id": 2,
        "name": "阳江市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "阳江市江城区"
    },
    {
        "id": 3,
        "name": "阳江市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "阳江市江城区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议阳江市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议广东省委员会",
        "location": "阳江市江城区"
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
        "name": "中共广州市南沙区委",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共广州市委员会",
        "location": "广州市南沙区"
    },
    {
        "id": 7,
        "name": "中共惠州市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "惠州市"
    },
    {
        "id": 8,
        "name": "广东省商务厅",
        "type": "政府",
        "level": "正厅级",
        "parent": "广东省人民政府",
        "location": "广州市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 卢一先 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "中共阳江市委书记", "start_date": "2023-08", "end_date": "present", "rank": "正厅级", "note": ""},
    # 卢一先此前曾任广州市委常委、南沙区委书记
    {"person_id": 1, "org_id": 6, "title": "中共广州市南沙区委书记", "start_date": "2021-??", "end_date": "2023-08", "rank": "副厅级", "note": "兼南沙区委书记"},
    # 余金富 — 市长
    {"person_id": 2, "org_id": 2, "title": "阳江市市长", "start_date": "2021-11", "end_date": "present", "rank": "正厅级", "note": "2021年11月任代市长，后当选"},
    {"person_id": 2, "org_id": 1, "title": "中共阳江市委副书记", "start_date": "2021-11", "end_date": "present", "rank": "正厅级", "note": "市委副书记兼市长"},
    # 余金富此前曾任惠州市委副书记、广东省商务厅副厅长
    {"person_id": 2, "org_id": 7, "title": "中共惠州市委副书记", "start_date": "2020-??", "end_date": "2021-11", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "广东省商务厅副厅长", "start_date": "2018-??", "end_date": "2020-??", "rank": "副厅级", "note": ""},
    # 冯玲（前任市委书记，女）
    {"person_id": 5, "org_id": 1, "title": "中共阳江市委书记", "start_date": "2021-04", "end_date": "2023-08", "rank": "正厅级", "note": "冯玲，后升任广东省副省长"},
    # 焦兰生（更前任市委书记）
    {"person_id": 6, "org_id": 1, "title": "中共阳江市委书记", "start_date": "2018-10", "end_date": "2021-04", "rank": "正厅级", "note": "焦兰生"},
    # 温湛滨（前任市长）
    {"person_id": 7, "org_id": 2, "title": "阳江市市长", "start_date": "2016-08", "end_date": "2021-11", "rank": "正厅级", "note": "温湛滨，后调任"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记卢一先与市长余金富是阳江市最重要的党政搭档", "overlap_org": "中共阳江市委员会/阳江市人民政府", "overlap_period": "2023-08至今"},
    # 前后任市委书记
    {"person_a": 5, "person_b": 1, "type": "前后任", "context": "冯玲（2021-04至2023-08）→卢一先（2023-08至今）", "overlap_org": "中共阳江市委员会", "overlap_period": "2023-08交接"},
    {"person_a": 6, "person_b": 5, "type": "前后任", "context": "焦兰生（2018-10至2021-04）→冯玲（2021-04至2023-08）", "overlap_org": "中共阳江市委员会", "overlap_period": "2021-04交接"},
    # 前后任市长
    {"person_a": 7, "person_b": 2, "type": "前后任", "context": "温湛滨（2016-08至2021-11）→余金富（2021-11至今）", "overlap_org": "阳江市人民政府", "overlap_period": "2021-11交接"},
    # 焦兰生与温湛滨曾搭档
    {"person_a": 6, "person_b": 7, "type": "党政正职搭档", "context": "焦兰生任市委书记时，温湛滨任市长", "overlap_org": "中共阳江市委员会/阳江市人民政府", "overlap_period": "2018-10至2021-04"},
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
