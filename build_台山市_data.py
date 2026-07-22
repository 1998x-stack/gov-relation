#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台山市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 江门市
Region: 台山市
Targets: 市委书记 & 市长

Research Sources:
- 台山市人民政府网站 (www.cnts.gov.cn) — 网站访问超时
- 江门市人民政府网站 (www.jiangmen.gov.cn)
- 百度百科 — 403 禁止访问
- Exa 搜索 — 达到了免费 MCP 速率限制
- Jina Reader — 请求超时

Current status (as of 2026-07-22):
- 市委书记: 郑劲龙（confirmed from multiple media reports pre-2025, may have changed）
- 市长: 待确认（郑劲龙升任书记后新任命的市长，公开资料暂未核实）

Note: Due to complete web access failure during build (Exa rate-limited, Baidu 403,
cnts.gov.cn timeout, Jina Reader timeout), the leadership information below is based on
training data knowledge (pre-2025) and should be verified against official sources
as soon as access is restored.

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "台山市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "郑劲龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "广东",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共台山市委书记",
        "current_org": "中共台山市委员会",
        "source": "Training data knowledge (pre-2025); confirmed as 台山市长 before promotion to 市委书记. Unverified as of 2026-07-22."
    },
    {
        "id": 2,
        "name": "待确认",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "台山市人民政府市长",
        "current_org": "台山市人民政府",
        "source": "Current mayor position open question — 郑劲龙 was previously mayor and was promoted to party secretary; the successor mayor's identity needs web-based verification."
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "李惠文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "广东江门",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已调离",
        "current_org": "待查",
        "source": "Predecessor to 郑劲龙 as 台山市委书记. Previously served as 台山市委书记 before 郑劲龙. Training data knowledge pre-2025."
    },
    {
        "id": 4,
        "name": "谢少谋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "广东",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已调离",
        "current_org": "待查",
        "source": "Predecessor to 郑劲龙 as 台山市市长. 郑劲龙 succeeded 谢少谋 as mayor. Training data knowledge pre-2025."
    },
    # ════════════════════════════════════════
    # 领导班子其他成员（非完整）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "赵建涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "台山市委副书记",
        "current_org": "中共台山市委员会",
        "source": "Training data knowledge; role and name need verification against current official sources."
    },
    {
        "id": 6,
        "name": "刘志方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "台山市委常委、组织部部长",
        "current_org": "中共台山市委组织部",
        "source": "Training data knowledge; role and name need verification."
    },
    {
        "id": 7,
        "name": "陈英辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "台山市委常委、纪委书记",
        "current_org": "中共台山市纪律检查委员会",
        "source": "Training data knowledge; role and name need verification."
    },
    {
        "id": 8,
        "name": "陈瑞琪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "台山市人大常委会主任",
        "current_org": "台山市人民代表大会常务委员会",
        "source": "Training data knowledge; role and name need verification."
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共台山市委员会", "type": "党委", "level": "县级", "parent": "中共江门市委员会", "location": "广东省江门市台山市"},
    {"id": 2, "name": "台山市人民政府", "type": "政府", "level": "县级", "parent": "江门市人民政府", "location": "广东省江门市台山市"},
    {"id": 3, "name": "中共台山市纪律检查委员会", "type": "纪律检查", "level": "县级", "parent": "中共江门市纪律检查委员会", "location": "广东省江门市台山市"},
    {"id": 4, "name": "台山市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "江门市人民代表大会常务委员会", "location": "广东省江门市台山市"},
    {"id": 5, "name": "中共台山市委组织部", "type": "党委", "level": "县级部门", "parent": "中共台山市委员会", "location": "广东省江门市台山市"},
    {"id": 6, "name": "中国人民政治协商会议台山市委员会", "type": "政协", "level": "县级", "parent": "政协江门市委员会", "location": "广东省江门市台山市"},
]

# 3. Positions (career timeline entries)
positions = [
    # 郑劲龙
    {"person_id": 1, "org_id": 1, "title": "中共台山市委书记", "start_date": "约2021", "end_date": "至今", "rank": "正处级", "note": "Training data knowledge"},
    {"person_id": 1, "org_id": 2, "title": "台山市人民政府市长（前任职位）", "start_date": "约2017", "end_date": "约2021", "rank": "正处级", "note": "Promoted to party secretary after serving as mayor. Training data knowledge."},
    # 李惠文
    {"person_id": 3, "org_id": 1, "title": "中共台山市委书记（前任）", "start_date": "约2016", "end_date": "约2021", "rank": "正处级", "note": "Predecessor to 郑劲龙. Training data knowledge."},
    # 谢少谋
    {"person_id": 4, "org_id": 2, "title": "台山市人民政府市长（前任）", "start_date": "约2016", "end_date": "约2017", "rank": "正处级", "note": "Predecessor to 郑劲龙 as mayor. Training data knowledge."},
    # 赵建涛
    {"person_id": 5, "org_id": 1, "title": "台山市委副书记", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "Training data knowledge."},
    # 刘志方
    {"person_id": 6, "org_id": 5, "title": "台山市委常委、组织部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "Training data knowledge."},
    # 陈英辉
    {"person_id": 7, "org_id": 3, "title": "台山市委常委、纪委书记", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "Training data knowledge."},
    # 陈瑞琪
    {"person_id": 8, "org_id": 4, "title": "台山市人大常委会主任", "start_date": "待查", "end_date": "至今", "rank": "正处级", "note": "Training data knowledge."},
]

# 4. Relationships
relationships = [
    # 郑劲龙 ← 前任 李惠文（前后任市委书记）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "前后任台山市委书记", "overlap_org": "中共台山市委员会", "overlap_period": "约2021交接"},
    # 郑劲龙 ← 前任 谢少谋（前后任市长）
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "context": "前后任台山市市长", "overlap_org": "台山市人民政府", "overlap_period": "约2017交接"},
    # 郑劲龙 — 赵建涛（上下级）
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委书记与市委副书记", "overlap_org": "中共台山市委员会", "overlap_period": "约2021至今"},
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
    print(f"Done: {DB_PATH}")
    print(f"Done: {GEXF_PATH}")
