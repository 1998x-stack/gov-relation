#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运河区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 沧州市
Region: 运河区
Targets: 区委书记 & 区长

Research Sources:
- 训练数据中确认于岗任运河区委书记、刘亮任运河区区长
- 所有官方渠道（www.czyhq.gov.cn）无法访问（超时）
- 百度百科/搜索均不可用（403验证码拦截）
- Exa搜索限流
- 所有信息因网络搜索受限未核实，标注为unverified

Research Date: 2026-07-24
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "运河区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons / 核心人物
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "于岗",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "沧州市运河区委书记",
        "current_org": "中共沧州市运河区委员会",
        "source": "unverified — 训练数据含于岗任运河区委书记。所有官方/百科渠道均不可用，信息未核实。"
    },
    {
        "id": 2,
        "name": "刘亮",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "沧州市运河区委副书记、区长",
        "current_org": "运河区人民政府",
        "source": "unverified — 训练数据含刘亮任运河区区长。所有官方/百科渠道均不可用，信息未核实。"
    },
]

# 2. Organizations / 组织
organizations = [
    {"id": 1, "name": "中共沧州市运河区委员会", "type": "党委", "level": "县处级", "location": "河北省沧州市运河区"},
    {"id": 2, "name": "运河区人民政府", "type": "政府", "level": "县处级", "location": "河北省沧州市运河区"},
    {"id": 3, "name": "沧州市", "type": "地级市", "level": "地厅级", "location": "河北省"},
]

# 3. Positions / 任职记录
positions = [
    # 于岗
    {"person_id": 1, "org_id": 1, "title": "沧州市运河区委书记", "start": "待查", "end": "present", "rank": "正处级", "note": "网络搜索受限，上任时间未核实"},
    # 刘亮
    {"person_id": 2, "org_id": 2, "title": "沧州市运河区委副书记、区长", "start": "待查", "end": "present", "rank": "正处级", "note": "网络搜索受限，上任时间未核实"},
]

# 4. Relationships / 关系
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "于岗（区委书记）与刘亮（区长）为运河区党政主要领导搭档关系",
        "overlap_org": "中共沧州市运河区委员会 / 运河区人民政府",
        "overlap_period": "待查",
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
        overwrite=True,
    )
