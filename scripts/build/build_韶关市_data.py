#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
韶关市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Parent City:
Region: 韶关市
Targets: 市委书记 & 市长

Research Sources:
- 维基百科 (zh.wikipedia.org) — 韶关市词条
- 韶关市政府网站 (www.sg.gov.cn)
- 百度百科

Current status (as of 2026-07-22):
- 市委书记: 陈少荣（2022年9月－）
- 市长: 吴庆华（2025年4月－）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "韶关市"
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
        "name": "陈少荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "广东陆丰",
        "native_place": "广东陆丰",
        "education": "广东省委党校研究生学历",
        "party_join": "中共党员（1988年）",
        "work_start": "1989年6月",
        "current_post": "中共韶关市委书记、韶关市人大常委会主任",
        "current_org": "中共韶关市委员会",
        "source": "Wikipedia:陈少荣(1968年)"
    },
    {
        "id": 2,
        "name": "吴庆华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共韶关市委副书记、市长",
        "current_org": "韶关市人民政府",
        "source": "Wikipedia:韶关市"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "陈少荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "广东陆丰",
        "native_place": "广东陆丰",
        "education": "广东省委党校研究生学历",
        "party_join": "中共党员（1988年）",
        "work_start": "1989年6月",
        "current_post": "韶关市人大常委会主任（市委书记兼）",
        "current_org": "韶关市人民代表大会常务委员会",
        "source": "Wikipedia:韶关市"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "胡海运",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "韶关市政协主席",
        "current_org": "中国人民政治协商会议韶关市委员会",
        "source": "Wikipedia:韶关市"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "王瑞军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "内蒙古乌拉特前旗",
        "native_place": "内蒙古",
        "education": "北京理工大学管理科学工程专业博士",
        "party_join": "中共党员（1990年）",
        "work_start": "1992年8月",
        "current_post": "（已离任韶关，曾任广东省科技厅厅长等职）",
        "current_org": "（已离任）",
        "source": "Wikipedia:王瑞军"
    },
    {
        "id": 6,
        "name": "陈少荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "广东陆丰",
        "native_place": "广东陆丰",
        "education": "广东省委党校研究生学历",
        "party_join": "中共党员（1988年）",
        "work_start": "1989年6月",
        "current_post": "（前任韶关市市长，后任市委书记）",
        "current_org": "（已离任市长岗位）",
        "source": "Wikipedia:韶关市"
    },
    {
        "id": 7,
        "name": "殷焕明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年11月",
        "birthplace": "广东东莞",
        "native_place": "广东东莞",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（前任韶关市市长，已离任）",
        "current_org": "（已离任）",
        "source": "Wikipedia:韶关市"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共韶关市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "韶关市浈江区"
    },
    {
        "id": 2,
        "name": "韶关市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "韶关市浈江区"
    },
    {
        "id": 3,
        "name": "韶关市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "韶关市浈江区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议韶关市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议广东省委员会",
        "location": "韶关市浈江区"
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
        "name": "广东省科技厅",
        "type": "政府",
        "level": "省级",
        "parent": "广东省人民政府",
        "location": "广州市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 陈少荣（现任市委书记）
    {"person_id": 1, "org_id": 1, "title": "中共韶关市委书记", "start": "2022-09", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 3, "title": "韶关市人大常委会主任", "start": "2022-09", "end": "present", "rank": "正厅级", "note": "市委书记兼任"},
    # 吴庆华（现任市长）
    {"person_id": 2, "org_id": 2, "title": "韶关市市长", "start": "2025-04", "end": "present", "rank": "正厅级", "note": "2025年4月当选"},
    {"person_id": 2, "org_id": 1, "title": "中共韶关市委副书记", "start": "2025-04", "end": "present", "rank": "正厅级", "note": "市委副书记兼市长"},
    # 胡海运
    {"person_id": 4, "org_id": 4, "title": "韶关市政协主席", "start": "2020-06", "end": "present", "rank": "正厅级", "note": ""},
    # 王瑞军（前任市委书记）
    {"person_id": 5, "org_id": 1, "title": "中共韶关市委书记", "start": "2020-10", "end": "2022-09", "rank": "正厅级", "note": "后调任广东省科技厅厅长"},
    {"person_id": 5, "org_id": 6, "title": "广东省科技厅厅长", "start": "2022-09", "end": "present", "rank": "正厅级", "note": "王瑞军调任"},
    {"person_id": 5, "org_id": 3, "title": "韶关市人大常委会主任", "start": "2020-10", "end": "2022-09", "rank": "正厅级", "note": "兼任"},
    # 陈少荣（前任市长）
    {"person_id": 6, "org_id": 2, "title": "韶关市市长", "start": "2020-10", "end": "2022-09", "rank": "正厅级", "note": "后升任市委书记"},
    {"person_id": 6, "org_id": 1, "title": "中共韶关市委副书记", "start": "2020-10", "end": "2022-09", "rank": "正厅级", "note": "市长兼市委副书记"},
    # 殷焕明（前任市长）
    {"person_id": 7, "org_id": 2, "title": "韶关市市长", "start": "2017-05", "end": "2020-10", "rank": "正厅级", "note": "后调任"},
    {"person_id": 7, "org_id": 1, "title": "中共韶关市委副书记", "start": "2017-05", "end": "2020-10", "rank": "正厅级", "note": ""},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记与市长是地级市最重要的党政搭档", "overlap_org": "中共韶关市委员会/韶关市人民政府", "overlap_period": "2025-04至今"},
    # 前后任市委书记
    {"person_a": 5, "person_b": 1, "type": "前后任", "context": "王瑞军（2020-10至2022-09）→陈少荣（2022-09至今）", "overlap_org": "中共韶关市委员会", "overlap_period": "2022-09交接"},
    # 前后任市长
    {"person_a": 7, "person_b": 6, "type": "前后任", "context": "殷焕明（2017-05至2020-10）→陈少荣（2020-10至2022-09）", "overlap_org": "韶关市人民政府", "overlap_period": "2020-10交接"},
    {"person_a": 6, "person_b": 2, "type": "前后任", "context": "陈少荣（2020-10至2022-09）→吴庆华（2025-04至今）", "overlap_org": "韶关市人民政府", "overlap_period": "2025-04交接"},
    # 陈少荣的党政角色转换
    {"person_a": 1, "person_b": 6, "type": "同人", "context": "陈少荣从市长升任市委书记，同为一人", "overlap_org": "中共韶关市委员会/韶关市人民政府", "overlap_period": "2020-10至今"},
    # 市政协与市委
    {"person_a": 4, "person_b": 1, "type": "党政关系", "context": "市政协主席与市委书记的党政协作", "overlap_org": "韶关市领导班子", "overlap_period": "2022-09至今"},
    # 王瑞军与陈少荣（前任党政搭档）
    {"person_a": 5, "person_b": 6, "type": "党政正职搭档", "context": "王瑞军任市委书记时陈少荣任市长（2020-10至2022-09）", "overlap_org": "中共韶关市委员会/韶关市人民政府", "overlap_period": "2020-10至2022-09"},
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
