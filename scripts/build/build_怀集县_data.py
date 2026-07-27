#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
怀集县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 肇庆市
Region: 怀集县
Targets: 县委书记 & 县长

Research Sources:
- 怀集县人民政府网站 (www.huaiji.gov.cn) — 领导之窗栏目
- 怀集发布新闻文章 (2025-2026)
- 百度百科 — 403 禁止访问

Current status (as of 2026-07-22):
- 县委书记: 空缺（前任于晓军，最后公开出现为2025年11月；2026年1月起由县长陈腾达代行县委常委会工作）
- 县长: 陈腾达（confirmed from official news articles 2026-07-15）
- 县委副书记（专职）: 张帮繁

Note: 
- 县委书记于晓军于2025年11月仍主持县委常委会，2026年1月县委全会由陈腾达代表县委常委会作工作报告
- 此后县委常委会均由陈腾达（县委副书记、县长）主持，县委书记岗位显示为空缺或调整中
- 领导之窗（县政府网站）列出了7位领导：陈腾达、魏繁强、黄文锋、李媚、黄志伟、陈剑锋、钟兆茂
- 因web访问受限（Exa rate-limited, Baidu 403），详细履历信息基于官方新闻报道

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "怀集县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 核心领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "陈腾达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共怀集县委副书记、县长",
        "current_org": "怀集县人民政府",
        "source": "怀集县人民政府网站领导之窗; 怀集发布新闻 (2026-07-15县委常委会); 2026-01-26县委全会。身份 confirmed 但详细履历待查。自2026年1月起代行县委常委会工作。"
    },
    {
        "id": 2,
        "name": "于晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原中共怀集县委书记（已于2025年底离任）",
        "current_org": "不详",
        "source": "怀集发布新闻 (2025-11-06县委常委会、2025-11-25冷坑镇宣讲、2025-12-09园区调研)。最后公开出现为2025年12月。2026年1月起不再担任县委书记。"
    },
    # ════════════════════════════════════════
    # 县委其他领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "张帮繁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县委副书记（专职）",
        "current_org": "中共怀集县委员会",
        "source": "怀集发布新闻 (2026-07-01两优一先表彰大会、2026-07-06全县领导干部警示教育会)。确认任专职副书记。"
    },
    {
        "id": 4,
        "name": "魏繁强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县委常委、常务副县长",
        "current_org": "怀集县人民政府",
        "source": "怀集县人民政府网站领导之窗; 2026-01-26县委全会经济工作专题讲话。确认任县委常委、常务副县长。"
    },
    {
        "id": 5,
        "name": "黎方祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县委常委、宣传部部长",
        "current_org": "中共怀集县委宣传部",
        "source": "怀集发布新闻 (2026-07-19金燕文化嘉年华致辞; 2026-07-13应急演练)。确认任县委常委、宣传部部长。"
    },
    {
        "id": 6,
        "name": "黄文锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县领导（待确认具体职务）",
        "current_org": "怀集县",
        "source": "怀集县人民政府网站领导之窗。具体职务待确认。"
    },
    {
        "id": 7,
        "name": "李媚",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县领导（待确认具体职务）",
        "current_org": "怀集县",
        "source": "怀集县人民政府网站领导之窗; 怀集发布新闻 (2026-07-17县委理论学习中心组学习会作学习发言)。"
    },
    {
        "id": 8,
        "name": "黄志伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县领导（待确认具体职务）",
        "current_org": "怀集县",
        "source": "怀集县人民政府网站领导之窗。具体职务待确认。"
    },
    {
        "id": 9,
        "name": "陈剑锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县领导（待确认具体职务）",
        "current_org": "怀集县",
        "source": "怀集县人民政府网站领导之窗。具体职务待确认。"
    },
    {
        "id": 10,
        "name": "钟兆茂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县领导（待确认具体职务）",
        "current_org": "怀集县",
        "source": "怀集县人民政府网站领导之窗; 怀集发布新闻 (2026-07-17县委理论学习中心组学习会作学习发言)。"
    },
    # ════════════════════════════════════════
    # 县其他领导
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "冯永忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县人大常委会主任（推测）",
        "current_org": "怀集县人民代表大会常务委员会",
        "source": "怀集发布新闻 (2026-07-19金燕文化嘉年华、2026-07-17县委理论学习中心组学习会)。作为县领导出席，推测为人大会主任。"
    },
    {
        "id": 12,
        "name": "程云区",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县政协主席（推测）",
        "current_org": "中国人民政治协商会议怀集县委员会",
        "source": "怀集发布新闻 (2026-07-19金燕文化嘉年华、2026-07-17县委理论学习中心组学习会)。作为县领导出席，推测为政协主席。"
    },
    {
        "id": 13,
        "name": "高广泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县领导（待确认具体职务）",
        "current_org": "怀集县",
        "source": "怀集发布新闻 (2026-07-19金燕文化嘉年华)。作为县领导出席。"
    },
    {
        "id": 14,
        "name": "江建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县领导（待确认具体职务）",
        "current_org": "怀集县",
        "source": "怀集发布新闻 (2025-11-14全省农田建设现场会)。作为县领导出席。"
    },
    {
        "id": 15,
        "name": "李奇洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "怀集县领导（待确认具体职务）",
        "current_org": "怀集县",
        "source": "怀集发布新闻 (2025-11-14全省农田建设现场会)。作为县领导出席。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共怀集县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共肇庆市委员会",
        "location": "广东省肇庆市怀集县"
    },
    {
        "id": 2,
        "name": "怀集县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "肇庆市人民政府",
        "location": "广东省肇庆市怀集县"
    },
    {
        "id": 3,
        "name": "怀集县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "肇庆市人民代表大会常务委员会",
        "location": "广东省肇庆市怀集县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议怀集县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议肇庆市委员会",
        "location": "广东省肇庆市怀集县"
    },
    {
        "id": 5,
        "name": "中共怀集县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共怀集县委员会",
        "location": "广东省肇庆市怀集县"
    },
]

# 3. Positions
positions = [
    # 陈腾达（id=1）
    {"person_id": 1, "org_id": 2, "title": "怀集县县长", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "怀集县委副书记", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "自2026年1月起主持县委常委会工作"},
    # 于晓军（id=2）— 前任县委书记
    {"person_id": 2, "org_id": 1, "title": "怀集县委书记", "start_date": "待查", "end_date": "2025-12", "rank": "正处级", "note": "最后公开出现为2025年12月"},
    # 张帮繁（id=3）
    {"person_id": 3, "org_id": 1, "title": "怀集县委副书记（专职）", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 魏繁强（id=4）
    {"person_id": 4, "org_id": 2, "title": "怀集县常务副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "怀集县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 黎方祥（id=5）
    {"person_id": 5, "org_id": 5, "title": "怀集县委宣传部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "怀集县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 黄文锋（id=6）
    {"person_id": 6, "org_id": 1, "title": "怀集县领导（具体职务待确认）", "start_date": "待查", "end_date": "现在", "rank": "待查", "note": ""},
    # 李媚（id=7）
    {"person_id": 7, "org_id": 1, "title": "怀集县领导（具体职务待确认）", "start_date": "待查", "end_date": "现在", "rank": "待查", "note": ""},
    # 黄志伟（id=8）
    {"person_id": 8, "org_id": 1, "title": "怀集县领导（具体职务待确认）", "start_date": "待查", "end_date": "现在", "rank": "待查", "note": ""},
    # 陈剑锋（id=9）
    {"person_id": 9, "org_id": 1, "title": "怀集县领导（具体职务待确认）", "start_date": "待查", "end_date": "现在", "rank": "待查", "note": ""},
    # 钟兆茂（id=10）
    {"person_id": 10, "org_id": 1, "title": "怀集县领导（具体职务待确认）", "start_date": "待查", "end_date": "现在", "rank": "待查", "note": ""},
    # 冯永忠（id=11）
    {"person_id": 11, "org_id": 3, "title": "怀集县人大常委会主任（推测）", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": "身份为推测，需确认"},
    # 程云区（id=12）
    {"person_id": 12, "org_id": 4, "title": "怀集县政协主席（推测）", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": "身份为推测，需确认"},
    # 高广泽（id=13）
    {"person_id": 13, "org_id": 1, "title": "怀集县领导（具体职务待确认）", "start_date": "待查", "end_date": "现在", "rank": "待查", "note": ""},
    # 江建军（id=14）
    {"person_id": 14, "org_id": 1, "title": "怀集县领导（具体职务待确认）", "start_date": "待查", "end_date": "现在", "rank": "待查", "note": ""},
    # 李奇洪（id=15）
    {"person_id": 15, "org_id": 1, "title": "怀集县领导（具体职务待确认）", "start_date": "待查", "end_date": "现在", "rank": "待查", "note": ""},
]

# 4. Relationships
relationships = [
    # 陈腾达与前任书记
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县长与县委书记搭档关系（2025年及之前）",
        "overlap_org": "中共怀集县委员会",
        "overlap_period": "2025年及之前"
    },
    # 陈腾达与专职副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与专职副书记搭档关系",
        "overlap_org": "中共怀集县委员会",
        "overlap_period": "2026年"
    },
    # 陈腾达与常务副县长
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与常务副县长搭档关系",
        "overlap_org": "怀集县人民政府",
        "overlap_period": "2026年"
    },
    # 陈腾达与宣传部长
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县长与宣传部长上下级关系",
        "overlap_org": "中共怀集县委员会",
        "overlap_period": "2026年"
    },
    # 陈腾达与人大会主任（推测）
    {
        "person_a": 1,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "县长与人大主任同班子关系",
        "overlap_org": "怀集县",
        "overlap_period": "2026年"
    },
    # 陈腾达与政协主席（推测）
    {
        "person_a": 1,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "县长与政协主席同班子关系",
        "overlap_org": "怀集县",
        "overlap_period": "2026年"
    },
    # 李媚与钟兆茂（同时在学习会上发言）
    {
        "person_a": 7,
        "person_b": 10,
        "type": "overlap",
        "context": "同在县委理论学习中心组学习会作学习发言",
        "overlap_org": "中共怀集县委员会",
        "overlap_period": "2026-07-17"
    },
    # 张帮繁与黎方祥
    {
        "person_a": 3,
        "person_b": 5,
        "type": "overlap",
        "context": "同在县委任职",
        "overlap_org": "中共怀集县委员会",
        "overlap_period": "2026年"
    },
    # 魏繁强与陈腾达（经济工作配合）
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与常务副县长的经济工作配合关系",
        "overlap_org": "怀集县人民政府",
        "overlap_period": "2026年"
    },
]


if __name__ == "__main__":
    # ── Determine output paths (staging mode) ──
    db = DB_PATH
    gexf = GEXF_PATH

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db,
        gexf_path=gexf,
        overwrite=True,
    )
    print(f"\nDone. Database: {db}")
    print(f"GEXF: {gexf}")
