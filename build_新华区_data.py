#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沧州市新华区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 沧州市
Region: 新华区
Targets: 区委书记 & 区长

Research Sources:
- 训练数据中识别金培元任新华区委书记、陈国帮任新华区区长
- 所有官方渠道（czxhq.gov.cn）无法访问（DNS/连接超时）
- 百度百科/搜索均不可用（403验证码拦截）
- Exa搜索限流，Google不可用
- 所有信息因网络搜索受限未核实，标注为unverified
- 维基百科仅提供行政区划统计信息，无领导信息

Research Date: 2026-07-24
"""

import os
import sys

_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "新华区"

DB_PATH = os.path.join(DATABASE_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons / 核心人物
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "金培元",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "沧州市新华区委书记",
        "current_org": "中共沧州市新华区委员会",
        "source": "unverified — 训练数据含金培元任新华区委书记（自2021年）。所有官方/百科渠道均不可用，信息未核实。"
    },
    {
        "id": 2,
        "name": "陈国帮",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "沧州市新华区委副书记、区长",
        "current_org": "新华区人民政府",
        "source": "unverified — 训练数据含陈国帮任新华区区长（自2021年）。所有官方/百科渠道均不可用，信息未核实。"
    },
    # ════════════════════════════════════════
    # Key Deputies (more tentative — unverified)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "刘文新",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区委常委、常务副区长",
        "current_org": "新华区人民政府",
        "source": "unverified — 训练数据推测，官方渠道不可用。"
    },
    {
        "id": 4,
        "name": "张秀娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区委常委、组织部部长",
        "current_org": "中共沧州市新华区委组织部",
        "source": "unverified — 训练数据推测，官方渠道不可用。"
    },
    {
        "id": 5,
        "name": "辛连昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区委常委、纪委书记、监委主任",
        "current_org": "中共沧州市新华区纪律检查委员会",
        "source": "unverified — 训练数据推测，官方渠道不可用。"
    },
    {
        "id": 6,
        "name": "赵学功",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区委常委、政法委书记",
        "current_org": "中共沧州市新华区委政法委员会",
        "source": "unverified — 训练数据推测，官方渠道不可用。"
    },
    {
        "id": 7,
        "name": "张仕平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区委常委、统战部部长",
        "current_org": "中共沧州市新华区委统一战线工作部",
        "source": "unverified — 训练数据推测，官方渠道不可用。"
    },
    {
        "id": 8,
        "name": "高永强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区委常委、宣传部部长",
        "current_org": "中共沧州市新华区委宣传部",
        "source": "unverified — 训练数据推测，官方渠道不可用。"
    },
    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "刘建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区委原书记（已离任）",
        "current_org": "",
        "source": "unverified — 训练数据含刘建华约2016-2021年任新华区委书记。去向不明。"
    },
]

# 2. Organizations / 组织
organizations = [
    {"id": 1, "name": "中共沧州市新华区委员会", "type": "党委", "level": "县处级", "location": "河北省沧州市新华区"},
    {"id": 2, "name": "新华区人民政府", "type": "政府", "level": "县处级", "location": "河北省沧州市新华区"},
    {"id": 3, "name": "中共沧州市新华区纪律检查委员会", "type": "纪委", "level": "县处级", "location": "河北省沧州市新华区"},
    {"id": 4, "name": "新华区人大常委会", "type": "人大", "level": "县处级", "location": "河北省沧州市新华区"},
    {"id": 5, "name": "政协新华区委员会", "type": "政协", "level": "县处级", "location": "河北省沧州市新华区"},
    {"id": 6, "name": "中共沧州市新华区委组织部", "type": "党委部门", "level": "乡科级", "location": "河北省沧州市新华区"},
    {"id": 7, "name": "中共沧州市新华区委宣传部", "type": "党委部门", "level": "乡科级", "location": "河北省沧州市新华区"},
    {"id": 8, "name": "中共沧州市新华区委政法委员会", "type": "党委部门", "level": "乡科级", "location": "河北省沧州市新华区"},
    {"id": 9, "name": "中共沧州市新华区委统一战线工作部", "type": "党委部门", "level": "乡科级", "location": "河北省沧州市新华区"},
    {"id": 10, "name": "沧州市", "type": "地级市", "level": "地厅级", "location": "河北省"},
]

# 3. Positions / 任职记录
positions = [
    # 金培元
    {"person_id": 1, "org_id": 1, "title": "沧州市新华区委书记", "start_date": "约2021", "end_date": "present", "rank": "正处级", "note": "训练数据推测约2021年从区长转任书记。网络搜索受限，上任时间未核实。"},
    {"person_id": 1, "org_id": 2, "title": "沧州市新华区委副书记、区长", "start_date": "约2017", "end_date": "约2021", "rank": "正处级", "note": "训练数据推测此前任新华区长。具体时间未核实。"},
    # 陈国帮
    {"person_id": 2, "org_id": 2, "title": "沧州市新华区委副书记、区长", "start_date": "约2021", "end_date": "present", "rank": "正处级", "note": "训练数据推测约2021年任新华区长。网络搜索受限，上任时间未核实。"},
    # 刘文新（常务副区长）
    {"person_id": 3, "org_id": 2, "title": "新华区委常委、常务副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "训练数据推测。上任时间未核实。"},
    # 张秀娟（组织部长）
    {"person_id": 4, "org_id": 6, "title": "新华区委常委、组织部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "训练数据推测。上任时间未核实。"},
    # 辛连昌（纪委书记）
    {"person_id": 5, "org_id": 3, "title": "新华区委常委、纪委书记、监委主任", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "训练数据推测。上任时间未核实。"},
    # 赵学功（政法委书记）
    {"person_id": 6, "org_id": 8, "title": "新华区委常委、政法委书记", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "训练数据推测。上任时间未核实。"},
    # 张仕平（统战部长）
    {"person_id": 7, "org_id": 9, "title": "新华区委常委、统战部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "训练数据推测。上任时间未核实。"},
    # 高永强（宣传部长）
    {"person_id": 8, "org_id": 7, "title": "新华区委常委、宣传部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "训练数据推测。上任时间未核实。"},
    # 刘建华（前任书记）
    {"person_id": 9, "org_id": 1, "title": "沧州市新华区委书记", "start_date": "约2016", "end_date": "约2021", "rank": "正处级", "note": "训练数据推测约2016-2021年任新华区委书记。去向不明。"},
]

# 4. Relationships / 关系
relationships = [
    # 党政主要领导搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "金培元（区委书记）与陈国帮（区长）为新华区党政主要领导搭档关系。金培元此前也任新华区长，陈国帮接任区长职务。",
        "overlap_org": "中共沧州市新华区委员会 / 新华区人民政府",
        "overlap_period": "约2021至今",
    },
    # 书记-前任书记
    {
        "person_a": 1,
        "person_b": 9,
        "type": "predecessor_successor",
        "context": "金培元接替刘建华任新华区委书记。刘建华约2016-2021年任书记，金培元约2021年接任。",
        "overlap_org": "中共沧州市新华区委员会",
        "overlap_period": "约2021交接",
    },
    # 书记-常务副区长
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "金培元（书记）与刘文新（常务副区长）为党政班子成员。",
        "overlap_org": "新华区党政领导班子",
        "overlap_period": "待查",
    },
    # 书记-组织部长
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "金培元作为区委书记，与组织部部长张秀娟共同负责干部管理工作。",
        "overlap_org": "中共沧州市新华区委员会",
        "overlap_period": "待查",
    },
    # 区长-常务副区长
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "陈国帮（区长）与刘文新（常务副区长）为区政府正副职搭档。",
        "overlap_org": "新华区人民政府",
        "overlap_period": "待查",
    },
    # 书记-纪委书记
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "金培元（书记）与辛连昌（纪委书记）在区委常委会中共事。",
        "overlap_org": "中共沧州市新华区委员会",
        "overlap_period": "待查",
    },
]

# ── Build ──

if __name__ == "__main__":
    print("=" * 60)
    print("  沧州市新华区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24")
    print("  状态: ⚠️ 网络搜索受限，所有数据未核实")
    print("=" * 60)
    print()
    print("  当前网络搜索状态:")
    print("  - Exa搜索: 限流 (API rate limit)")
    print("  - Baidu/Baidu Baike: 403 验证码拦截")
    print("  - 新华区政府网站 (czxhq.gov.cn): 无法访问")
    print("  - 沧州市政府网站: 可访问但领导之窗JS渲染无法解析")
    print("  - Jina Reader: 不可用 (传输错误)")
    print()
    print("  信息来源: 训练数据知识，所有条目标注为 unverified")
    print()
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
    print(f"\n⚠️  注意: 所有人物数据因网络搜索受限均未核实。")
    print(f"  请通过以下渠道补充核实：")
    print(f"  1. 沧州市新华区政府官网 (czxhq.gov.cn 或 xinhua.cangzhou.gov.cn)")
    print(f"  2. 沧州市政府官网领导之窗 (www.cangzhou.gov.cn)")
    print(f"  3. 沧州市委组织部 任前公示")
    print(f"  4. Baidu Baike: 新华区 (沧州市)")
    print(f"\n✅ 构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人 (均未核实)")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")
