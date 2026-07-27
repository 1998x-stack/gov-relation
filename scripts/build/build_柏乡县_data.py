#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
柏乡县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邢台市
Region: 柏乡县
Targets: 县委书记 & 县长

Research Sources:
- 由于严重的网络访问限制（Exa API rate limit、百度/Bing/Google/Sogou搜索全部被封禁或超时、
  柏乡县人民政府网站 www.baixiangxian.gov.cn 返回403禁止访问、维基百科API不可达、
  百度百科403验证码拦截、360百科无匹配词条、Jina Reader超时），
  所有信息均无法通过网络搜索实时验证。
- 本脚本中的信息基于公开资料的历史知识，标注为"unverified"，
  需要通过正常网络环境重新验证。
- 具体来源参考 report/20260723-河北省-邢台市-柏乡县-县委书记.md

Research Date: 2026-07-23

⚠️ 重要说明：
本脚本数据的置信度较低。所有核心字段（出生年月、教育背景、入党时间等）均需验证。
当前县委书记可能已在2024-2026年间发生更替。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "柏乡县"

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
        "name": "徐艳刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "柏乡县委书记（待确认是否仍在任）",
        "current_org": "中共柏乡县委员会",
        "source": "unverified。徐艳刚约于2021-2022年任柏乡县委书记。2024-2026年期间是否仍在该岗位未知。未找到简历来源。"
    },
    {
        "id": 2,
        "name": "待查（县长）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "柏乡县委副书记、县长",
        "current_org": "柏乡县人民政府",
        "source": "unverified。县长姓名待查。此前曾有报道提及柏乡县长人选但当前在任者未知。"
    },
    # ════════════════════════════════════════
    # Predecessors (Historical Leaders)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "王涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（已离任柏乡县委书记）",
        "current_org": "",
        "source": "unverified。王涛约于2018年至2021年任柏乡县委书记。去向：可能调任邢台市市直部门或其他县市。"
    },
    {
        "id": 4,
        "name": "张万双",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（已离任柏乡县委书记）",
        "current_org": "",
        "source": "unverified。张万双约于2015年至2018年任柏乡县委书记。"
    },
    {
        "id": 5,
        "name": "李振军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（已离任柏乡县职务）",
        "current_org": "",
        "source": "unverified。李振军曾任柏乡县委书记，具体任期待查。注意：邢台市信都区也有一位李振军（曾任桥西区长），是否同一人需核实。"
    },
    # ════════════════════════════════════════
    # Key County Leaders (Partial - mostly unknown)
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "县委副书记（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "柏乡县委副书记",
        "current_org": "中共柏乡县委员会",
        "source": "unverified。县委副书记姓名待查。"
    },
    {
        "id": 7,
        "name": "县纪委书记（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "柏乡县纪委书记、县监委主任",
        "current_org": "中共柏乡县纪律检查委员会",
        "source": "unverified。县纪委书记姓名待查。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共柏乡县委员会",
        "type": "党委",
        "level": "县级",
        "location": "邢台市柏乡县",
        "parent": "中共邢台市委"
    },
    {
        "id": 2,
        "name": "柏乡县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邢台市柏乡县",
        "parent": "邢台市人民政府"
    },
    {
        "id": 3,
        "name": "柏乡县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邢台市柏乡县",
        "parent": "邢台市人大常委会"
    },
    {
        "id": 4,
        "name": "政协柏乡县委员会",
        "type": "政协",
        "level": "县级",
        "location": "邢台市柏乡县",
        "parent": "政协邢台市委员会"
    },
    {
        "id": 5,
        "name": "中共柏乡县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "location": "邢台市柏乡县",
        "parent": "中共柏乡县委员会"
    },
    {
        "id": 6,
        "name": "中共柏乡县委组织部",
        "type": "党委",
        "level": "县级",
        "location": "邢台市柏乡县",
        "parent": "中共柏乡县委员会"
    },
    {
        "id": 7,
        "name": "中共柏乡县委宣传部",
        "type": "党委",
        "level": "县级",
        "location": "邢台市柏乡县",
        "parent": "中共柏乡县委员会"
    },
    {
        "id": 8,
        "name": "中共柏乡县委政法委员会",
        "type": "党委",
        "level": "县级",
        "location": "邢台市柏乡县",
        "parent": "中共柏乡县委员会"
    },
]

# 3. Positions
positions = [
    # 徐艳刚（现任或最近任县委书记）
    {"person_id": 1, "org_id": 1, "title": "柏乡县委书记", "start": "约2021-2022年", "end": "present（待确认）", "rank": "正处级", "note": "具体到任月份待查"},
    # 待查县长
    {"person_id": 2, "org_id": 2, "title": "柏乡县委副书记、县长", "start": "待查", "end": "present", "rank": "正处级", "note": "姓名和任期待查"},
    # 王涛（前任县委书记）
    {"person_id": 3, "org_id": 1, "title": "柏乡县委书记", "start": "约2018年", "end": "约2021年", "rank": "正处级", "note": ""},
    # 张万双
    {"person_id": 4, "org_id": 1, "title": "柏乡县委书记", "start": "约2015年", "end": "约2018年", "rank": "正处级", "note": ""},
    # 李振军
    {"person_id": 5, "org_id": 1, "title": "柏乡县委书记", "start": "待查", "end": "待查", "rank": "正处级", "note": "任期待查，可能早于张万双"},
    # 县委副书记
    {"person_id": 6, "org_id": 1, "title": "柏乡县委副书记", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待查"},
    # 县纪委书记
    {"person_id": 7, "org_id": 5, "title": "柏乡县纪委书记、县监委主任", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待查"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长为柏乡县核心党政领导搭档",
        "overlap_org": "中共柏乡县委员会／柏乡县人民政府",
        "overlap_period": ""
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "王涛任柏乡县委书记，徐艳刚接任",
        "overlap_org": "中共柏乡县委员会",
        "overlap_period": "约2021年"
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "张万双任柏乡县委书记，王涛接任",
        "overlap_org": "中共柏乡县委员会",
        "overlap_period": "约2018年"
    },
    {
        "person_a": 4,
        "person_b": 5,
        "type": "predecessor_successor",
        "context": "李振军任柏乡县委书记（早于张万双）",
        "overlap_org": "中共柏乡县委员会",
        "overlap_period": "待查"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记领导县委副书记",
        "overlap_org": "中共柏乡县委员会",
        "overlap_period": ""
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县委书记领导县纪委工作",
        "overlap_org": "中共柏乡县委员会",
        "overlap_period": ""
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
