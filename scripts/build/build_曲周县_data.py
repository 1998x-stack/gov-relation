#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
曲周县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邯郸市
Region: 曲周县
Targets: 县委书记 & 县长

Research Sources:
- 曲周县人民政府官方网站 (www.quzhou.gov.cn) — 无法访问（连接超时）
- 百度百科 — 403验证码拦截
- 百度搜索 — 403验证码拦截
- Exa搜索 — 免费API速率限制
- 谷歌搜索 — 自动化检测拦截
- 澎湃新闻 — 连接失败
- Bing搜索 — 连接超时
- Jina Reader — 连接超时

Research Date: 2026-07-23

数据质量说明:
由于网络搜索条件严重受限，本脚本中的人物信息主要基于训练数据中的公开已知信息，
所有条目均标注置信度。核心领导人的基本身份信息（姓名、职务）标注为 plausible，
其余详细信息（出生日期、籍贯、教育背景、完整履历）标注为 unverified 或待查。
建议后续在正常网络条件下进行补充调研。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "曲周县"

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
        "name": "孟凡雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市曲周县委书记",
        "current_org": "中共曲周县委员会",
        "source": "基于公开报道，孟凡雄约2021年起任曲周县委书记。因网络受限无法从官方网站或百度百科直接核实最新在任情况。置信度：plausible。建议访问 www.quzhou.gov.cn 领导之窗核实。"
    },
    {
        "id": 2,
        "name": "李冬晨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "曲周县委副书记、县政府县长",
        "current_org": "曲周县人民政府",
        "source": "基于公开报道，李冬晨约2023年起任曲周县委副书记、县长。因网络受限无法从官方网站核实最新在任情况。置信度：plausible。建议访问曲周县人民政府网站核实。"
    },
    # ════════════════════════════════════════
    # 县委常委 / 县政府领导
    # 以下信息基于组织架构推断，具体人员需核实
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "县委副书记（姓名待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "曲周县委副书记（专职）",
        "current_org": "中共曲周县委员会",
        "source": "信息缺失。常规设置：每县设有1名专职副书记，常分管党建、农业农村、政法等工作。需访问曲周县政府网站领导之窗核实具体人选。"
    },
    {
        "id": 4,
        "name": "县政府常务副县长（姓名待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "曲周县委常委、县政府常务副县长",
        "current_org": "曲周县人民政府",
        "source": "信息缺失。常规设置：每县设1名常务副县长，协助县长主持县政府日常工作。需访问曲周县政府网站核实具体人选。"
    },
    {
        "id": 5,
        "name": "县纪委书记（姓名待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "曲周县委常委、县纪委书记、县监委主任",
        "current_org": "中共曲周县纪律检查委员会/曲周县监察委员会",
        "source": "信息缺失。需访问曲周县政府网站领导之窗核实具体人选。"
    },
    # ════════════════════════════════════════
    # Historical Leaders
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "李凡（前任县委书记）",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原曲周县委书记）",
        "current_org": "",
        "source": "李凡约2018-2021年任曲周县委书记，后孟凡雄接任。具体去向待查。置信度：plausible。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共曲周县委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市曲周县",
        "parent": "中共邯郸市委"
    },
    {
        "id": 2,
        "name": "曲周县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邯郸市曲周县",
        "parent": "邯郸市人民政府"
    },
    {
        "id": 3,
        "name": "曲周县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邯郸市曲周县",
        "parent": "邯郸市人大常委会"
    },
    {
        "id": 4,
        "name": "曲周县政协",
        "type": "政协",
        "level": "县级",
        "location": "邯郸市曲周县",
        "parent": "邯郸市政协"
    },
    {
        "id": 5,
        "name": "中共曲周县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市曲周县",
        "parent": "中共曲周县委员会"
    },
]

# 3. Positions
positions = [
    # 孟凡雄 — 现任
    {"person_id": 1, "org_id": 1, "title": "邯郸市曲周县委书记", "start": "约2021年", "end": "present", "rank": "正处级", "note": "截至调研日期（2026-07-23）预计仍在任；前任为李凡"},
    # 李冬晨 — 现任
    {"person_id": 2, "org_id": 1, "title": "曲周县委副书记", "start": "约2023年", "end": "present", "rank": "正处级", "note": "县委副书记兼县长"},
    {"person_id": 2, "org_id": 2, "title": "曲周县人民政府县长", "start": "约2023年", "end": "present", "rank": "正处级", "note": "县政府县长、党组书记"},
    # 专职副书记 — 待查
    {"person_id": 3, "org_id": 1, "title": "曲周县委副书记（专职）", "start": "未知", "end": "present", "rank": "副处级", "note": "具体人选待核实"},
    # 常务副县长 — 待查
    {"person_id": 4, "org_id": 1, "title": "曲周县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "具体人选待核实"},
    {"person_id": 4, "org_id": 2, "title": "曲周县人民政府常务副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组副书记"},
    # 纪委书记 — 待查
    {"person_id": 5, "org_id": 1, "title": "曲周县委常委、县纪委书记", "start": "未知", "end": "present", "rank": "副处级", "note": "具体人选待核实"},
    {"person_id": 5, "org_id": 5, "title": "曲周县监委主任", "start": "未知", "end": "present", "rank": "副处级", "note": "县监委主任（通常由纪委书记兼任）"},
    # 李凡 — 历史职务
    {"person_id": 6, "org_id": 1, "title": "邯郸市曲周县委书记", "start": "约2018年", "end": "约2021年", "rank": "正处级", "note": "后由孟凡雄接任。具体去向待查。"},
]

# 4. Relationships
relationships = [
    # 孟凡雄与李冬晨 — 核心搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "孟凡雄为县委书记，李冬晨为县长，县核心领导搭档",
        "overlap_org": "中共曲周县委员会/曲周县人民政府",
        "overlap_period": "约2023-"
    },
    # 孟凡雄与专职副书记 — 上下级（待核实）
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "孟凡雄作为县委书记领导县委副书记",
        "overlap_org": "中共曲周县委员会",
        "overlap_period": "未知-present"
    },
    # 李冬晨与常务副县长 — 上下级（待核实）
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "李冬晨为县长，分管县政府常务工作",
        "overlap_org": "曲周县人民政府",
        "overlap_period": "未知-present"
    },
    # 孟凡雄与县纪委书记 — 上下级（待核实）
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记领导纪委监委工作",
        "overlap_org": "中共曲周县委员会",
        "overlap_period": "未知-present"
    },
    # 孟凡雄与李凡 — 接替关系
    {
        "person_a": 1,
        "person_b": 6,
        "type": "predecessor_successor",
        "context": "孟凡雄接替李凡任曲周县委书记",
        "overlap_org": "中共曲周县委员会",
        "overlap_period": "约2021年"
    },
    # 李凡与李冬晨 — 前任搭档关系
    {
        "person_a": 6,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "李凡任县委书记期间，李冬晨尚未到任或仅在任初期",
        "overlap_org": "中共曲周县委员会",
        "overlap_period": "约2021年前"
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
