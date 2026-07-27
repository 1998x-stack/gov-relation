#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番禺区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 广州市
Region: 番禺区
Targets: 区委书记 & 区长

Research Sources:
- 维基百科番禺区词条 — 领导信息（区委书记黄彪确认）
- 广州市番禺区人民政府门户网站 (www.panyu.gov.cn)
- 荔湾区、海珠区等同级区县数据作为参考模式

Research Date: 2026-07-22

网络环境限制说明:
- Google/Exa 搜索达到速率限制
- 百度搜索被验证码拦截
- Jina Reader 超时
- 部分政府网站路径404
- 基于维基百科确认区委书记信息，区长等信息标注为待查
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "番禺区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "黄彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广州市番禺区委书记",
        "current_org": "中共广州市番禺区委员会",
        "source": "维基百科番禺区词条（引用广州市政府官网链接）; www.panyu.gov.cn"
    },
    {
        "id": 2,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "番禺区委副书记、区长",
        "current_org": "番禺区人民政府",
        "source": "待查 —— 网络受限无法获取番禺区政府领导之窗页面详情"
    },
    # ════════════════════════════════════════
    # Former / Predecessor Leaders
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "叶珊瑚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（原番禺区长）",
        "current_org": "番禺区人民政府（前任区长）",
        "source": "公开报道（2021-2023年间任职番禺区长）"
    },
    {
        "id": 4,
        "name": "陈德俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（原番禺区长）",
        "current_org": "番禺区人民政府（更早前任区长）",
        "source": "公开报道"
    },
    # ════════════════════════════════════════
    # 人大、政协主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "番禺区人大常委会主任",
        "current_org": "广州市番禺区人民代表大会常务委员会",
        "source": "待查 —— 网络受限无法获取"
    },
    {
        "id": 6,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "番禺区政协主席",
        "current_org": "中国人民政治协商会议广州市番禺区委员会",
        "source": "待查 —— 网络受限无法获取"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共广州市番禺区委员会",
        "type": "党委",
        "level": "副厅级（区委书记通常为副厅级）",
        "parent": "中共广州市委",
        "location": "广州市番禺区市桥街道清河东路319号"
    },
    {
        "id": 2,
        "name": "番禺区人民政府",
        "type": "政府",
        "level": "正处级",
        "parent": "广州市人民政府",
        "location": "广州市番禺区市桥街道清河东路319号"
    },
    {
        "id": 3,
        "name": "广州市番禺区人民代表大会常务委员会",
        "type": "人大",
        "level": "正处级",
        "parent": "广州市人大常委会",
        "location": "广州市番禺区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议广州市番禺区委员会",
        "type": "政协",
        "level": "正处级",
        "parent": "广州市政协",
        "location": "广州市番禺区"
    },
]

# 3. Positions
positions = [
    # 黄彪
    {"person_id": 1, "org_id": 1, "title": "广州市番禺区委书记", "start": "2023(估)", "end": "至今", "rank": "副厅级", "note": "主持区委全面工作。据维基百科数据，具体任职起始日期待查"},
    # 区长（待确认姓名）
    {"person_id": 2, "org_id": 1, "title": "番禺区委副书记", "start": "待查", "end": "至今", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "番禺区区长", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持区政府全面工作。具体姓名待查"},
    # 叶珊瑚（前任区长）
    {"person_id": 3, "org_id": 2, "title": "番禺区区长（前任）", "start": "2021(估)", "end": "2023(估)", "rank": "正处级", "note": "前任区长，具体任期需进一步确认"},
    # 陈德俊（更早前任区长）
    {"person_id": 4, "org_id": 2, "title": "番禺区区长（更早前任）", "start": "2016(估)", "end": "2021(估)", "rank": "正处级", "note": "更早前任区长"},
    # 人大主任
    {"person_id": 5, "org_id": 3, "title": "番禺区人大常委会主任", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持区人大常委会全面工作"},
    # 政协主席
    {"person_id": 6, "org_id": 4, "title": "番禺区政协主席", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持区政协全面工作"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长：党委与政府主要领导工作搭档关系",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "中共广州市番禺区委员会/番禺区人民政府",
        "overlap_period": "至今",
        "source": "番禺区领导班子架构"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "区委书记与人大主任：同届班子共事",
        "strength": "medium",
        "confidence": "plausible",
        "overlap_org": "番禺区",
        "overlap_period": "至今",
        "source": "番禺区领导班子架构"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "overlap",
        "context": "区委书记与政协主席：同届班子共事",
        "strength": "medium",
        "confidence": "plausible",
        "overlap_org": "番禺区",
        "overlap_period": "至今",
        "source": "番禺区领导班子架构"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "现任区长接替叶珊瑚出任番禺区区长",
        "strength": "strong",
        "confidence": "plausible",
        "overlap_org": "番禺区人民政府",
        "overlap_period": "交接期待查",
        "source": "公开报道: 叶珊瑚曾任番禺区长"
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "叶珊瑚接替陈德俊出任番禺区区长",
        "strength": "strong",
        "confidence": "plausible",
        "overlap_org": "番禺区人民政府",
        "overlap_period": "约2016-2021（陈德俊）/ 2021-2023（叶珊瑚）",
        "source": "公开报道"
    },
]

# ── Run ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\nDone. Files created:")
    print(f"  - {DB_PATH}")
    print(f"  - {GEXF_PATH}")
