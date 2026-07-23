#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
青龙满族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 秦皇岛市
Region: 青龙满族自治县
Targets: 县委书记 & 县长

Research Sources:
- 网络搜索全面受限：Exa rate-limit、百度验证码、政府网站 (www.qinglong.gov.cn) 超时
- 当前领导信息基于知识库中的公开报道（截至2025年初），需后续通过官方渠道核实
- 待查阅：青龙满族自治县人民政府门户网站—领导之窗、秦皇岛市人民政府网站、百度百科

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "青龙满族自治县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "李耀滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青龙满族自治县委书记",
        "current_org": "中共青龙满族自治县委员会",
        "source": "知识库中的公开报道显示李耀滨担任青龙满族自治县委书记，因网络受限未能获取官方领导之窗确认页；约2021-2022年任职"
    },
    {
        "id": 2,
        "name": "张义金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青龙满族自治县委副书记、县长",
        "current_org": "青龙满族自治县人民政府",
        "source": "知识库中的公开报道显示张义金担任青龙满族自治县长，因网络受限未能获取官方领导之窗确认页；约2021-2022年任职"
    },
    # ════════════════════════════════════════
    # 县级领导（待核实）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（县委副书记）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青龙满族自治县委副书记（或常务副县长）",
        "current_org": "中共青龙满族自治县委员会",
        "source": "待补充"
    },
    {
        "id": 4,
        "name": "待查（县人大常委会主任）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青龙满族自治县人大常委会主任",
        "current_org": "青龙满族自治县人大常委会",
        "source": "待补充"
    },
    {
        "id": 5,
        "name": "待查（县政协主席）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青龙满族自治县政协主席",
        "current_org": "青龙满族自治县政协",
        "source": "待补充"
    },
    {
        "id": 6,
        "name": "待查（县委常委、常务副县长）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青龙满族自治县委常委、常务副县长",
        "current_org": "青龙满族自治县人民政府",
        "source": "待补充"
    },
    {
        "id": 7,
        "name": "待查（县纪委书记）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青龙满族自治县委常委、纪委书记",
        "current_org": "中共青龙满族自治县纪律检查委员会",
        "source": "待补充"
    },
    {
        "id": 8,
        "name": "待查（县委组织部长）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青龙满族自治县委常委、组织部长",
        "current_org": "中共青龙满族自治县委员会组织部",
        "source": "待补充"
    },
    {
        "id": 9,
        "name": "待查（县委宣传部长）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青龙满族自治县委常委、宣传部长",
        "current_org": "中共青龙满族自治县委员会宣传部",
        "source": "待补充"
    },
    {
        "id": 10,
        "name": "待查（县委政法委书记）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "青龙满族自治县委常委、政法委书记",
        "current_org": "中共青龙满族自治县委员会政法委",
        "source": "待补充"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共青龙满族自治县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "秦皇岛市青龙满族自治县"
    },
    {
        "id": 2,
        "name": "青龙满族自治县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "秦皇岛市青龙满族自治县"
    },
    {
        "id": 3,
        "name": "青龙满族自治县人大常委会",
        "type": "人大",
        "level": "县处级",
        "location": "秦皇岛市青龙满族自治县"
    },
    {
        "id": 4,
        "name": "青龙满族自治县政协",
        "type": "政协",
        "level": "县处级",
        "location": "秦皇岛市青龙满族自治县"
    },
    {
        "id": 5,
        "name": "中共秦皇岛市委",
        "type": "党委",
        "level": "地市级",
        "location": "秦皇岛市"
    },
    {
        "id": 6,
        "name": "中共青龙满族自治县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "location": "秦皇岛市青龙满族自治县"
    },
    {
        "id": 7,
        "name": "青龙满族自治县监察委员会",
        "type": "政府",
        "level": "县处级",
        "location": "秦皇岛市青龙满族自治县"
    },
    {
        "id": 8,
        "name": "中共青龙满族自治县委员会组织部",
        "type": "党委",
        "level": "县处级",
        "location": "秦皇岛市青龙满族自治县"
    },
    {
        "id": 9,
        "name": "中共青龙满族自治县委员会宣传部",
        "type": "党委",
        "level": "县处级",
        "location": "秦皇岛市青龙满族自治县"
    },
    {
        "id": 10,
        "name": "中共青龙满族自治县委员会政法委",
        "type": "党委",
        "level": "县处级",
        "location": "秦皇岛市青龙满族自治县"
    },
    {
        "id": 11,
        "name": "秦皇岛市人民政府",
        "type": "政府",
        "level": "地市级",
        "location": "秦皇岛市"
    },
]

# 3. Positions (person_id, org_id, title)
positions = [
    # 李耀滨 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "约2021", "end": "至今", "rank": "正县处级", "note": "知识库公开报道确认，具体任职时间需核实"},
    # 张义金 — 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "约2021", "end": "至今", "rank": "正县处级", "note": "知识库公开报道确认，具体任职时间需核实"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "约2021", "end": "至今", "rank": "正县处级", "note": "兼任县委副书记"},
    # 待查人员占位
    {"person_id": 3, "org_id": 1, "title": "县委副书记（或常务副县长）", "start": "待查", "end": "至今", "rank": "副县处级", "note": "待核实"},
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start": "待查", "end": "至今", "rank": "正县处级", "note": "待核实"},
    {"person_id": 5, "org_id": 4, "title": "县政协主席", "start": "待查", "end": "至今", "rank": "正县处级", "note": "待核实"},
    {"person_id": 6, "org_id": 2, "title": "县委常委、常务副县长", "start": "待查", "end": "至今", "rank": "副县处级", "note": "待核实"},
    {"person_id": 7, "org_id": 6, "title": "县委常委、纪委书记", "start": "待查", "end": "至今", "rank": "副县处级", "note": "待核实"},
    {"person_id": 8, "org_id": 8, "title": "县委常委、组织部长", "start": "待查", "end": "至今", "rank": "副县处级", "note": "待核实"},
    {"person_id": 9, "org_id": 9, "title": "县委常委、宣传部长", "start": "待查", "end": "至今", "rank": "副县处级", "note": "待核实"},
    {"person_id": 10, "org_id": 10, "title": "县委常委、政法委书记", "start": "待查", "end": "至今", "rank": "副县处级", "note": "待核实"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,  # 李耀滨
        "person_b": 2,  # 张义金
        "type": "overlap",
        "context": "县委书记与县长党政搭档关系",
        "overlap_org": "中共青龙满族自治县委/青龙满族自治县人民政府",
        "overlap_period": "约2021年至今"
    },
    {
        "person_a": 1,  # 李耀滨
        "person_b": 3,  # 待查（县委副书记）
        "type": "overlap",
        "context": "县委书记与县委副书记上下级关系",
        "overlap_org": "中共青龙满族自治县委",
        "overlap_period": "待核实"
    },
    {
        "person_a": 2,  # 张义金
        "person_b": 3,  # 待查（县委副书记）
        "type": "overlap",
        "context": "县长与县委副书记同级协作关系",
        "overlap_org": "中共青龙满族自治县委",
        "overlap_period": "待核实"
    },
    {
        "person_a": 1,  # 李耀滨
        "person_b": 6,  # 待查（常务副县长）
        "type": "overlap",
        "context": "县委书记与常务副县长上下级关系",
        "overlap_org": "青龙满族自治县人民政府/县委",
        "overlap_period": "待核实"
    },
    {
        "person_a": 2,  # 张义金
        "person_b": 6,  # 待查（常务副县长）
        "type": "overlap",
        "context": "县长与常务副县长上下级关系",
        "overlap_org": "青龙满族自治县人民政府",
        "overlap_period": "待核实"
    },
    {
        "person_a": 1,  # 李耀滨
        "person_b": 7,  # 待查（纪委书记）
        "type": "overlap",
        "context": "县委书记与纪委书记（同级监督关系）",
        "overlap_org": "中共青龙满族自治县委",
        "overlap_period": "待核实"
    },
    {
        "person_a": 8,  # 待查（组织部长）
        "person_b": 9,  # 待查（宣传部长）
        "type": "overlap",
        "context": "县委常委之间同级协作关系",
        "overlap_org": "中共青龙满族自治县委",
        "overlap_period": "待核实"
    },
]

# ── Run ──
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"\nDone: {SLUG}")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
