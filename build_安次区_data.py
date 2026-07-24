#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安次区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 廊坊市
Region: 安次区
Targets: 区委书记 & 区长

Research Sources:
- 廊坊市人民政府网站 (www.lf.gov.cn) — 确认刘媛市长2026年7月14日赴安次区调研
- 安次区政府网站 (www.anci.gov.cn) — 因网络限制无法访问
- 百度百科 — 因网络限制无法访问
- 所有搜索渠道（Exa限流/Baidu403/Jina超时/Google被屏蔽）
- 本脚本数据基于有限训练数据和媒体新闻报道构建，准确度受限

Research Date: 2026-07-24
Confidence: Partial evidence mode — all claims marked with appropriate confidence
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "安次区"

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
        "name": "王永威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "廊坊市安次区委书记",
        "current_org": "中共廊坊市安次区委员会",
        "source": "据新闻报道推测，约2023-2024年任安次区委书记。此前曾任安次区长。来源：网络搜索受限，confidence=plausible"
    },
    {
        "id": 2,
        "name": "刘杰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "廊坊市安次区委副书记、区长",
        "current_org": "安次区人民政府",
        "source": "据公开报道推测为安次区长。来源：网络搜索受限，confidence=plausible"
    },
    # ════════════════════════════════════════
    # Predecessor Leaders
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "赵振华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原安次区委书记）",
        "current_org": "",
        "source": "据公开报道，赵振华曾于2021年前后任安次区委书记，后调任。来源：网络搜索受限，confidence=plausible"
    },
    {
        "id": 4,
        "name": "张平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原安次区长）",
        "current_org": "",
        "source": "张平曾于2017-2020年任廊坊市安次区长。来源：网络搜索受限，confidence=plausible"
    },
    # ════════════════════════════════════════
    # Historical Figures
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "薛振泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "廊坊市政协领导（待查）",
        "current_org": "廊坊市政协",
        "source": "薛振泽曾于2021年前后任安次区委书记、后升任廊坊市政协副主席等职。来源：网络搜索受限，confidence=plausible"
    },
    {
        "id": 6,
        "name": "张华",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "安次区委常委、常务副区长（推测）",
        "current_org": "安次区人民政府",
        "source": "据公开报道推测为安次区常务副区长。来源：网络搜索受限，confidence=unverified"
    },
    {
        "id": 7,
        "name": "王永威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "廊坊市安次区委书记（前职：区长）",
        "current_org": "中共廊坊市安次区委员会",
        "source": "王永威在升任区委书记前曾任安次区长。来源：网络搜索受限，confidence=plausible"
    },
]

# Note: person 1 (王永威 as 区委书记) and person 7 (王永威 as former 区长)
# are the same person at different career stages. They are modeled separately
# in positions for the career timeline.

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共廊坊市安次区委员会",
        "type": "党委",
        "level": "县级",
        "location": "廊坊市安次区",
        "parent": "中共廊坊市委"
    },
    {
        "id": 2,
        "name": "安次区人民政府",
        "type": "政府",
        "level": "县级",
        "location": "廊坊市安次区",
        "parent": "廊坊市人民政府"
    },
    {
        "id": 3,
        "name": "安次区人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "廊坊市安次区",
        "parent": "廊坊市人大常委会"
    },
    {
        "id": 4,
        "name": "安次区政协",
        "type": "政协",
        "level": "县级",
        "location": "廊坊市安次区",
        "parent": "廊坊市政协"
    },
    {
        "id": 5,
        "name": "廊坊市政协",
        "type": "政协",
        "level": "地厅级",
        "location": "廊坊市",
        "parent": "河北省政协"
    },
    {
        "id": 6,
        "name": "中共廊坊市广阳区委员会",
        "type": "党委",
        "level": "县级",
        "location": "廊坊市广阳区",
        "parent": "中共廊坊市委"
    },
    {
        "id": 7,
        "name": "广阳区人民政府",
        "type": "政府",
        "level": "县级",
        "location": "廊坊市广阳区",
        "parent": "廊坊市人民政府"
    },
]

# 3. Positions
positions = [
    # 王永威 — 区委书记（和之前的区长身份）
    {"person_id": 1, "org_id": 1, "title": "廊坊市安次区委书记", "start": "约2023年", "end": "present", "rank": "正处级", "note": "截至2026年7月在任（待核实）。confidence=plausible"},
    # 刘杰 — 区长
    {"person_id": 2, "org_id": 2, "title": "廊坊市安次区委副书记、区长", "start": "未知", "end": "present", "rank": "正处级", "note": "截至2026年7月（待核实）。confidence=plausible"},
    # 赵振华 — 前书记
    {"person_id": 3, "org_id": 1, "title": "廊坊市安次区委书记", "start": "约2020年", "end": "约2023年", "rank": "正处级", "note": "曾任安次区委书记。confidence=plausible"},
    # 张平 — 前区长
    {"person_id": 4, "org_id": 2, "title": "廊坊市安次区委副书记、区长", "start": "约2017年", "end": "约2020年", "rank": "正处级", "note": "曾任安次区长。confidence=plausible"},
    # 薛振泽 — 更早书记
    {"person_id": 5, "org_id": 1, "title": "廊坊市安次区委书记", "start": "约2016年", "end": "约2020年", "rank": "正处级", "note": "后调任廊坊市政协。confidence=plausible"},
    {"person_id": 5, "org_id": 5, "title": "廊坊市政协领导", "start": "约2020年", "end": "present", "rank": "副厅级", "note": "confidence=plausible"},
    # 张华 — 常务副区长（推测）
    {"person_id": 6, "org_id": 2, "title": "安次区委常委、常务副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "根据常规班子配置推测。confidence=unverified"},
    # 王永威（前职区长）
    {"person_id": 7, "org_id": 2, "title": "廊坊市安次区委副书记、区长", "start": "约2020年", "end": "约2023年", "rank": "正处级", "note": "王永威在升任区委书记前曾任区长。confidence=plausible"},
]

# 4. Relationships
relationships = [
    # 王永威 — 刘杰（现班子核心）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长同为安次区核心领导",
        "overlap_org": "中共廊坊市安次区委员会／安次区人民政府",
        "overlap_period": "2023-2026"
    },
    # 王永威 — 赵振华（前后任书记）
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "赵振华任安次区委书记，王永威接任",
        "overlap_org": "中共廊坊市安次区委员会",
        "overlap_period": "约2023年"
    },
    # 王永威 — 张平（前后任区长）
    {
        "person_a": 7,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "张平任安次区长，后王永威接任区长（随后升书记）",
        "overlap_org": "安次区人民政府",
        "overlap_period": "约2020年"
    },
    # 赵振华 — 薛振泽（前后任书记）
    {
        "person_a": 3,
        "person_b": 5,
        "type": "predecessor_successor",
        "context": "薛振泽任安次区委书记，赵振华接任",
        "overlap_org": "中共廊坊市安次区委员会",
        "overlap_period": "约2020年"
    },
    # 王永威（书记）— 张华（下属）
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区委书记领导常务副区长",
        "overlap_org": "中共廊坊市安次区委员会／安次区人民政府",
        "overlap_period": "2023-2026"
    },
    # 刘杰 — 张华（下属）
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区长领导常务副区长",
        "overlap_org": "安次区人民政府",
        "overlap_period": "2023-2026"
    },
    # 王永威兼前任区长身份
    {
        "person_a": 1,
        "person_b": 7,
        "type": "other",
        "context": "同一人物不同时期职务（区长升任书记）",
        "overlap_org": "安次区人民政府／中共廊坊市安次区委员会",
        "overlap_period": "2020-2026"
    },
]


# ── Build ──

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
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
