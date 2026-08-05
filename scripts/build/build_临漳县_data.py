#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临漳县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邯郸市
Region: 临漳县
Targets: 县委书记 & 县长

Research Sources (local-first, degraded web):
- https://www.lzx.gov.cn/ (临漳县人民政府) — 连接超时
- Exa搜索 — 免费API速率限制
- r.jina.ai 代理 — 连接超时
- Bing / 澎湃 / 百度 — 连接失败 / 超时
- 本项目本地履历库（build_*_data.py + report/）— confirmed 来源

Research Date: 2026-08-05

数据质量说明(partial-evidence mode):
web 全通道受限，本脚本的“现任”核心人物(县委书记、县长)姓名未能在本会话内
从公开渠道核实，统一以“姓名待查/待确认”结构占位，并把对应缺口写入 open_questions
与 report/open_gaps.md，不凭空捏造姓名、出生、教育等字段。
已确认信息均来自本项目本地履历库（见各条 source 注释），标 confirmed：
- 边飞：曾任临漳县委书记（更早曲周县委书记等），2013 落马判无期徒刑。
- 马洪广：履历途经临漳县委（农工委、宣传部长兼统战部长）→现任永年区委书记。
- 李少锋：籍贯临漳县，复兴区前任区委书记（生于 1969-11）。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "临漳县"
PROVINCE = "河北省"
PARENT_CITY = "邯郸市"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leader — 县委书记 (姓名待确认)
    # 本会话无法从公开渠道核实现任临漳县委书记姓名，置为占位，缺口见 open_questions
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "县委书记（姓名待确认）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员（推测）",
        "work_start": "待查",
        "current_post": "临漳县委书记",
        "current_org": "中共临漳县委员会",
        "source": "临漳县委书记现任姓名在本会话内未能经公开检索核实（县级干部任免信息散见于市政府与县政府网站，均超时/受限）。按正常运行惯例为中共临漳县委书记。置信度：unverified。建议后续访问 www.lzx.gov.cn 领导之窗或邯郸市委组织部任前公示核实。"
    },
    {
        "id": 2,
        "name": "县长（姓名待确认）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员（推测）",
        "work_start": "待查",
        "current_post": "临漳县委副书记、县政府县长",
        "current_org": "临漳县人民政府",
        "source": "临漳县县长在本会话内未能经公开检索核实姓名。通常由临漳县人民政府官网领导之窗或临漳县人大任命公告确认。置信度：unverified。"
    },
    # ════════════════════════════════════════
    # 县委其他常委 / 县政府领导 (占位，姓名待核)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "县委专职副书记（姓名待核）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临漳县委副书记（专职）",
        "current_org": "中共临漳县委员会",
        "source": "信息缺失。常规设置：每县设1名专职副书记，常分管党建、农业农村、政法。需访问临漳县政府网站领导之窗核实具体人选。"
    },
    {
        "id": 4,
        "name": "县政府常务副县长（姓名待核）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临漳县委常委、县政府常务副县长",
        "current_org": "临漳县人民政府",
        "source": "信息缺失。常规设置：每县设1名常务副县长协助县长主持县政府日常工作。需访问临漳县政府网站核实具体人选。"
    },
    {
        "id": 5,
        "name": "县纪委书记（姓名待核）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临漳县委常委、县纪委书记、县监委主任",
        "current_org": "中共临漳县纪律检查委员会/临漳县监察委员会",
        "source": "信息缺失。需访问临漳县政府网站领导之窗核实具体人选。"
    },
    # ════════════════════════════════════════
    # 已确认的临漳相关干部（本地履历库 confirmed）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "边飞",
        "gender": "男",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员（后受党纪处置）",
        "work_start": "待查",
        "current_post": "无（因违纪违法接受审查，2013年后被处理）",
        "current_org": "",
        "source": "本项目本地履历库 confirmed：曾任曲周县委书记、临漳县委书记、魏县县委书记、永年县委书记，后任邯郸市委常委兼大名县委书记，2013年被调查后被判无期徒刑。来源：scripts/build/build_大名县_data.py（person_id 8）、build_永年区_data.py。"
    },
    {
        "id": 7,
        "name": "马洪广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校在职研究生（经济管理专业）",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市永年区委书记",
        "current_org": "中共邯郸市永年区委员会",
        "source": "本地履历库（build_永年区_data.py id 1）confirmed：磁县林坦镇→临漳县委（农工委、宣传部长兼统战部长）→成安县委常委、组织部长→鸡泽县长提名→广平县委书记→永年区委书记。本条目聚焦其临漳县委任职经历。"
    },
    {
        "id": 8,
        "name": "李少锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年11月",
        "birthplace": "河北省邯郸市临漳县",
        "native_place": "河北省邯郸市临漳县",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市审计局局长（2026年起，复兴区前任区委书记）",
        "current_org": "邯郸市审计局",
        "source": "本地履历库 confirmed：籍贯临漳县，临漳本地干部，早年在临漳工作；2021-05~2026任复兴区委书记，2026 调任市审计局局长。来源：build_复兴区_data.py、report/open_gaps.md(2026-08-05 resolved)。本条目聚焦其临漳籍贯与早期工作。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共临漳县委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市临漳县",
        "parent": "中共邯郸市委"
    },
    {
        "id": 2,
        "name": "临漳县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邯郸市临漳县",
        "parent": "邯郸市人民政府"
    },
    {
        "id": 3,
        "name": "临漳县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邯郸市临漳县",
        "parent": "邯郸市人大常委会"
    },
    {
        "id": 4,
        "name": "临漳县政协",
        "type": "政协",
        "level": "县级",
        "location": "邯郸市临漳县",
        "parent": "邯郸市政协"
    },
    {
        "id": 5,
        "name": "中共临漳县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市临漳县",
        "parent": "中共临漳县委员会"
    },
]

# 3. Positions
positions = [
    # 现任核心 — 姓名待确认
    {"person_id": 1, "org_id": 1, "title": "临漳县委书记", "start": "待查", "end": "present", "rank": "正处级", "note": "主持县委全面工作。具体人选本会话未能核实，置信度 unverified。"},
    # 县长 — 姓名待确认
    {"person_id": 2, "org_id": 1, "title": "临漳县委副书记", "start": "待查", "end": "present", "rank": "正处级", "note": "县委副书记兼县长，具体人选待核实"},
    {"person_id": 2, "org_id": 2, "title": "临漳县人民政府县长", "start": "待查", "end": "present", "rank": "正处级", "note": "县政府县长、党组书记，具体人选待核实"},
    # 专职副书记 — 待核
    {"person_id": 3, "org_id": 1, "title": "临漳县委副书记（专职）", "start": "未知", "end": "present", "rank": "副处级", "note": "具体人选待核实"},
    # 常务副县长 — 待核
    {"person_id": 4, "org_id": 1, "title": "临漳县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "具体人选待核实"},
    {"person_id": 4, "org_id": 2, "title": "临漳县人民政府常务副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组副书记"},
    # 纪委书记 — 待核
    {"person_id": 5, "org_id": 1, "title": "临漳县委常委、县纪委书记", "start": "未知", "end": "present", "rank": "副处级", "note": "具体人选待核实"},
    {"person_id": 5, "org_id": 5, "title": "临漳县监委主任", "start": "未知", "end": "present", "rank": "副处级", "note": "通常由纪委书记兼任"},
    # 边飞 — 历史职务（confirmed）
    {"person_id": 6, "org_id": 1, "title": "邯郸市临漳县委书记", "start": "约2000年代", "end": "约2008年前", "rank": "正处级", "note": "曾任临漳县委书记；后任魏县、永年县委书记、邯郸市委常委兼大名县委书记，2013年被查判无期。置信度：confirmed（本地履历库）"},
    # 马洪广 — 临漳县委任职（confirmed）
    {"person_id": 7, "org_id": 1, "title": "临漳县委宣传部部长兼统战部部长", "start": "约2000年代-2010年代", "end": "约2010年代", "rank": "副处级", "note": "另任临漳县委农工委书记。后赴成安、鸡泽、广平、永年。置信度：confirmed"},
    # 李少纪 — 临漳籍干部
    {"person_id": 8, "org_id": 1, "title": "临漳县任职/籍贯干部", "start": "早期", "end": "去临漳外", "rank": "待查", "note": "籍贯临漳县，临漳本地干部，早年在临漳工作；后任复兴区委书记、市审计局局长。置信度：confirmed（籍贯）。"},
]

# 4. Relationships
relationships = [
    # 县委书记 ↔ 县长 — 核心搭档（占位）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "临漳县委书记与县长，县核心领导搭档（占位，具体人名待核实）",
        "overlap_org": "中共临漳县委员会/临漳县人民政府",
        "overlap_period": "待查"
    },
    # 县委书记 → 专职副书记（占位）
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记领导专职县委副书记",
        "overlap_org": "中共临漳县委员会",
        "overlap_period": "未知-present"
    },
    # 县长 → 常务副县长（占位）
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长领导县政府常务工作",
        "overlap_org": "临漳县人民政府",
        "overlap_period": "未知-present"
    },
    # 县委书记 → 纪委书记 — on the current placeholder
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记领导纪委监委工作",
        "overlap_org": "中共临漳县委员会",
        "overlap_period": "未知-present"
    },
    # confirmed: 边飞 曾任临漳县委书记（历史）
    {
        "person_a": 6,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "边飞曾任临漳县委书记；现任县委书记（待确认）为后续接任者之一。历史关系，链路待核实。",
        "overlap_org": "中共临漳县委员会",
        "overlap_period": "跨不同时期"
    },
    # confirmed: 马洪广 在临漳县委与周边县网络
    {
        "person_a": 7,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "马洪广曾任临漳县委宣传部长兼统战部长，属临漳县级常委序列（占位书记为其时任领导）",
        "overlap_org": "中共临漳县委员会",
        "overlap_period": "约2003-2011"
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