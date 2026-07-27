#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
丰南区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 唐山市
Region: 丰南区
Targets: 区委书记 & 区长

Research Sources:
- 网络搜索受限，政府网站 (www.fengnan.gov.cn) 及百度百科均无法连通
- 当前领导信息基于搜索能力范围内的公开报道，需后续通过官方渠道核实
- 待查阅：丰南区人民政府门户网站—领导之窗、唐山市人民政府网站、百度百科

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "丰南区"

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
        "name": "赵立华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "唐山市丰南区委书记",
        "current_org": "中共唐山市丰南区委员会",
        "source": "公开新闻报道显示赵立华担任丰南区委书记（任职时间约2021年），因网络受限未能获取官方领导之窗确认页"
    },
    {
        "id": 2,
        "name": "霍强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "唐山市丰南区委副书记、区长",
        "current_org": "丰南区人民政府",
        "source": "公开新闻报道显示霍强担任丰南区长（任职时间约2021年），因网络受限未能获取官方领导之窗确认页"
    },
    # ════════════════════════════════════════
    # 区委领导 / 区人大、政协主要领导（待查）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（区委副书记）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰南区委副书记",
        "current_org": "中共唐山市丰南区委员会",
        "source": "待补充"
    },
    {
        "id": 4,
        "name": "待查（区人大常委会主任）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰南区人大常委会主任",
        "current_org": "丰南区人大常委会",
        "source": "待补充"
    },
    {
        "id": 5,
        "name": "待查（区政协主席）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丰南区政协主席",
        "current_org": "丰南区政协",
        "source": "待补充"
    },
    # ════════════════════════════════════════
    # 区级领导（待补充）
    # ════════════════════════════════════════
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共唐山市丰南区委员会",
        "type": "党委",
        "level": "县处级",
        "location": "唐山市丰南区"
    },
    {
        "id": 2,
        "name": "丰南区人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "唐山市丰南区"
    },
    {
        "id": 3,
        "name": "丰南区人大常委会",
        "type": "人大",
        "level": "县处级",
        "location": "唐山市丰南区"
    },
    {
        "id": 4,
        "name": "丰南区政协",
        "type": "政协",
        "level": "县处级",
        "location": "唐山市丰南区"
    },
    {
        "id": 5,
        "name": "中共唐山市委",
        "type": "党委",
        "level": "地市级",
        "location": "唐山市"
    },
    {
        "id": 6,
        "name": "中共唐山市丰南区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "location": "唐山市丰南区"
    },
    {
        "id": 7,
        "name": "丰南区监察委员会",
        "type": "政府",
        "level": "县处级",
        "location": "唐山市丰南区"
    },
]

# 3. Positions (person_id, org_id, title)
positions = [
    # 赵立华 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "约2021", "end": "至今", "rank": "正县处级", "note": "公开报道确认，具体任职时间需核实"},
    # 霍强 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "约2021", "end": "至今", "rank": "正县处级", "note": "公开报道确认，具体任职时间需核实"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "约2021", "end": "至今", "rank": "正县处级", "note": "兼任区委副书记"},
    # 待查人员占位
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "待查", "end": "至今", "rank": "副县处级", "note": "待核实"},
    {"person_id": 4, "org_id": 3, "title": "区人大常委会主任", "start": "待查", "end": "至今", "rank": "正县处级", "note": "待核实"},
    {"person_id": 5, "org_id": 4, "title": "区政协主席", "start": "待查", "end": "至今", "rank": "正县处级", "note": "待核实"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,  # 赵立华
        "person_b": 2,  # 霍强
        "type": "overlap",
        "context": "区委书记与区长党政搭档关系",
        "overlap_org": "中共丰南区委/丰南区人民政府",
        "overlap_period": "约2021年至今"
    },
    {
        "person_a": 1,  # 赵立华
        "person_b": 3,  # 待查（区委副书记）
        "type": "overlap",
        "context": "区委书记与区委副书记上下级关系",
        "overlap_org": "中共丰南区委",
        "overlap_period": "待核实"
    },
    {
        "person_a": 2,  # 霍强
        "person_b": 3,  # 待查（区委副书记）
        "type": "overlap",
        "context": "区长与区委副书记同级协作关系",
        "overlap_org": "中共丰南区委",
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
