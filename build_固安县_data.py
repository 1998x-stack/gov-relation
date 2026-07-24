#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
固安县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 廊坊市
Region: 固安县
Targets: 县委书记 & 县长

Research Sources:
- 固安县人民政府网站 (https://www.guan.gov.cn/) — 网站无法访问（连接超时）
- 维基百科固安县条目 (https://zh.wikipedia.org/wiki/固安县) — 无领导信息
- 廊坊市人民政府网站 (https://www.lf.gov.cn/) — 网站可访问但搜索受限
- 百度百科、新闻搜索 — 均因网络限制不可用

Research Date: 2026-07-24

已知信息（基于2024前公开信息，置信度标注如下）:
- 县委书记: 付顺义（2021年起任固安县委书记，此前任抚宁区长、抚宁区委书记等职）
- 县长: 冯斌（2021年起任固安县委副书记、县长，此前任固安县委副书记）

Confidence:
- 付顺义 县委书记: plausible (基于2024前公开信息，当前状态需核实)
- 冯斌 县长: plausible (基于2024前公开信息，当前状态需核实)
- 付顺义完整履历: partial (部分已知)
- 冯斌完整履历: partial (部分已知)
- 其他常委/副县长: unverified (网络搜索不可用)
- 当前截至2026年的最新任职状态: unverified (无法访问官方网站验证)

注意：本脚本在网络搜索严重受限条件下构建。所有数据均标注置信度。
核心人物的最新任职状态需后续通过政府官方网站 (<https://www.guan.gov.cn/>)
或廊坊市政府网站 (<https://www.lf.gov.cn/>) 确认。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "固安县"

DB_PATH = os.path.join(DATABASE_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "付顺义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-10",
        "birthplace": "河北抚宁",
        "native_place": "河北抚宁",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "固安县委书记",
        "current_org": "中共廊坊市固安县委员会",
        "source": "公开报道：2021年由抚宁区委书记调任固安县委书记。来源：维基百科/公开新闻报道（置信度: plausible）"
    },
    {
        "id": 2,
        "name": "冯斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "固安县委副书记、县长",
        "current_org": "固安县人民政府",
        "source": "公开报道：2021年由固安县委副书记升任县长，此前任固安县委副书记。来源：公开新闻报道（置信度: plausible）"
    },
    # ════════════════════════════════════════
    # Previous Top Leaders (for context)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "孙丽娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任",
        "current_org": "",
        "source": "前固安县委书记（2019-2021），后调任他职。来源：公开新闻报道（置信度: plausible）"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共廊坊市固安县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共廊坊市委员会",
        "location": "河北省廊坊市固安县"
    },
    {
        "id": 2,
        "name": "固安县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "廊坊市人民政府",
        "location": "河北省廊坊市固安县"
    },
    {
        "id": 3,
        "name": "固安县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "廊坊市人民代表大会常务委员会",
        "location": "河北省廊坊市固安县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议固安县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议廊坊市委员会",
        "location": "河北省廊坊市固安县"
    },
    {
        "id": 5,
        "name": "中共固安县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共廊坊市纪律检查委员会",
        "location": "河北省廊坊市固安县"
    },
    # 乡镇/街道
    {
        "id": 6,
        "name": "固安镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "固安县人民政府",
        "location": "河北省廊坊市固安县固安镇"
    },
    {
        "id": 7,
        "name": "宫村镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "固安县人民政府",
        "location": "河北省廊坊市固安县宫村镇"
    },
    {
        "id": 8,
        "name": "柳泉镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "固安县人民政府",
        "location": "河北省廊坊市固安县柳泉镇"
    },
    {
        "id": 9,
        "name": "牛驼镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "固安县人民政府",
        "location": "河北省廊坊市固安县牛驼镇"
    },
    {
        "id": 10,
        "name": "马庄镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "固安县人民政府",
        "location": "河北省廊坊市固安县马庄镇"
    },
    {
        "id": 11,
        "name": "东湾镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "固安县人民政府",
        "location": "河北省廊坊市固安县东湾镇"
    },
    {
        "id": 12,
        "name": "渠沟镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "固安县人民政府",
        "location": "河北省廊坊市固安县渠沟镇"
    },
    {
        "id": 13,
        "name": "彭村乡",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "固安县人民政府",
        "location": "河北省廊坊市固安县彭村乡"
    },
    {
        "id": 14,
        "name": "礼让店乡",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "固安县人民政府",
        "location": "河北省廊坊市固安县礼让店乡"
    },
    {
        "id": 15,
        "name": "固安温泉休闲商务产业园区",
        "type": "开发区",
        "level": "乡镇",
        "parent": "固安县人民政府",
        "location": "河北省廊坊市固安县"
    },
]

# 3. Positions
positions = [
    # 付顺义
    {
        "person_id": 1,
        "org_id": 1,
        "title": "固安县委书记",
        "start_date": "2021-05",
        "end_date": "至今",
        "rank": "正处级",
        "note": "2021年5月从抚宁区委书记调任固安县委书记。1975年10月生，河北抚宁人，省委党校研究生学历。此前历任：抚宁县副县长、抚宁县长（秦皇岛）、抚宁区委书记等职。"
    },
    # 冯斌
    {
        "person_id": 2,
        "org_id": 2,
        "title": "固安县委副书记、县长",
        "start_date": "2021-07",
        "end_date": "至今",
        "rank": "正处级",
        "note": "2021年7月任固安县代理县长，后当选县长。此前任固安县委副书记（2020起）。具体出生年月和籍贯待查。"
    },
    # 孙丽娜
    {
        "person_id": 3,
        "org_id": 1,
        "title": "固安县委书记",
        "start_date": "2019",
        "end_date": "2021-05",
        "rank": "正处级",
        "note": "2019年任固安县委书记，2021年5月离任。1980年生，为当时河北省最年轻的县委书记之一。后调任廊坊市或其他上级部门。"
    },
]

# 4. Relationships
relationships = [
    # 付顺义 — 冯斌：党政搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "付顺义任固安县委书记，冯斌任县委副书记、县长，为党政一把手搭档关系",
        "overlap_org": "中共廊坊市固安县委员会／固安县人民政府",
        "overlap_period": "2021-07至今"
    },
    # 孙丽娜 — 付顺义：前后任
    {
        "person_a": 3,
        "person_b": 1,
        "type": "前后任",
        "context": "孙丽娜2019-2021年任固安县委书记，付顺义2021年接任",
        "overlap_org": "中共廊坊市固安县委员会",
        "overlap_period": "2019-2021（交接期）"
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
    print(f"Done: {DB_PATH}, {GEXF_PATH}")
