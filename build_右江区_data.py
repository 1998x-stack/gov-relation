#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
右江区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 广西壮族自治区
Parent City: 百色市
Region: 右江区
Targets: 区委书记 & 区长

Research Note:
  右江区是百色市辖区，百色市委、市政府驻地。
  
  本次调查期间，右江区人民政府网站（http://www.youjiang.gov.cn/）DNS 解析失败，
  百色市人民政府网站（https://www.baise.gov.cn/）传输错误，
  Baidu Baike 返回 403 验证码拦截，
  Jina Reader 和 Exa 搜索均超时/限流。
  
  在当前网络环境下，无法获取右江区现任区委书记、区长姓名及领导班子信息。
  所有人员条目均为占位缺口（GAP），待网络恢复或通过其他渠道补充。

  右江区基本情况（来自已有知识）：
  - 右江区是百色市政治、经济、文化中心
  - 总面积约3,800平方公里，常住人口约40万
  - 区内有百色起义纪念园、百色水利枢纽等重要单位

Data Date: 2026-07-23
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Ensure gov_relation is importable ──
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ── Paths ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "右江区"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"
TODAY = AS_OF

# ═══════════════════════════════════════════════════════════════
# 1. PERSONS
# ═══════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记（GAP）
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "【待查】右江区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "右江区委书记（待查）",
        "current_org": "中共百色市右江区委员会",
        "source": "GAP — 官方网站 http://www.youjiang.gov.cn/ 无法访问（DNS 解析失败）；待后续通过百色市委组织部任前公示或领导之窗页面补充",
    },
    # ════════════════════════════════════════
    # 核心领导：区长（GAP）
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "【待查】右江区区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "右江区区长（待查）",
        "current_org": "百色市右江区人民政府",
        "source": "GAP — 官方网站 http://www.youjiang.gov.cn/ 无法访问；待后续补充",
    },
    # ════════════════════════════════════════
    # 区委副书记（GAP）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "【待查】右江区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "右江区委副书记（待查）",
        "current_org": "中共百色市右江区委员会",
        "source": "GAP — 待后续补充",
    },
    # ════════════════════════════════════════
    # 常务副区长（GAP）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "【待查】右江区常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "右江区委常委、常务副区长（待查）",
        "current_org": "百色市右江区人民政府",
        "source": "GAP — 待后续通过右江区政府领导之窗页面补充",
    },
    # ════════════════════════════════════════
    # 区纪委书记/监委主任（GAP）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "【待查】右江区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "右江区委常委、纪委书记、监委主任（待查）",
        "current_org": "中共百色市右江区纪律检查委员会",
        "source": "GAP — 待后续补充",
    },
    # ════════════════════════════════════════
    # 区委组织部长（GAP）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "【待查】右江区委组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "右江区委常委、组织部长（待查）",
        "current_org": "中共百色市右江区委组织部",
        "source": "GAP — 待后续补充",
    },
    # ════════════════════════════════════════
    # 区委宣传部长（GAP）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "【待查】右江区委宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "右江区委常委、宣传部长（待查）",
        "current_org": "中共百色市右江区委宣传部",
        "source": "GAP — 待后续补充",
    },
    # ════════════════════════════════════════
    # 区委政法委书记（GAP）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "【待查】右江区委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "右江区委常委、政法委书记（待查）",
        "current_org": "中共百色市右江区委政法委员会",
        "source": "GAP — 待后续补充",
    },
]

# ═══════════════════════════════════════════════════════════════
# 2. ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共百色市右江区委员会",
        "type": "党委",
        "level": "正处级",
        "parent": "中共百色市委员会",
        "location": "百色市右江区向阳路19号",
    },
    {
        "id": 2,
        "name": "百色市右江区人民政府",
        "type": "政府",
        "level": "正处级",
        "parent": "百色市人民政府",
        "location": "百色市右江区向阳路19号",
    },
    {
        "id": 3,
        "name": "中共百色市右江区纪律检查委员会",
        "type": "纪委",
        "level": "副处级",
        "parent": "中共百色市纪律检查委员会",
        "location": "百色市右江区",
    },
    {
        "id": 4,
        "name": "中共百色市右江区委组织部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共百色市右江区委员会",
        "location": "百色市右江区",
    },
    {
        "id": 5,
        "name": "中共百色市右江区委宣传部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共百色市右江区委员会",
        "location": "百色市右江区",
    },
    {
        "id": 6,
        "name": "中共百色市右江区委政法委员会",
        "type": "党委",
        "level": "正科级",
        "parent": "中共百色市右江区委员会",
        "location": "百色市右江区",
    },
    {
        "id": 7,
        "name": "百色市右江区人民代表大会常务委员会",
        "type": "人大",
        "level": "正处级",
        "parent": "百色市人民代表大会常务委员会",
        "location": "百色市右江区",
    },
    {
        "id": 8,
        "name": "中国人民政治协商会议百色市右江区委员会",
        "type": "政协",
        "level": "正处级",
        "parent": "中国人民政治协商会议百色市委员会",
        "location": "百色市右江区",
    },
]

# ═══════════════════════════════════════════════════════════════
# 3. POSITIONS
# ═══════════════════════════════════════════════════════════════

positions = [
    # GAP — 区委书记
    {"person_id": 1, "org_id": 1, "title": "右江区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 姓名和任职时间均未知"},
    # GAP — 区长
    {"person_id": 2, "org_id": 2, "title": "右江区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 姓名和任职时间均未知"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 待查"},
    # GAP — 副书记
    {"person_id": 3, "org_id": 1, "title": "右江区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 常务副区长
    {"person_id": 4, "org_id": 2, "title": "右江区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 纪委书记
    {"person_id": 5, "org_id": 3, "title": "右江区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 组织部长
    {"person_id": 6, "org_id": 4, "title": "右江区委常委、组织部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名未知"},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 宣传部长
    {"person_id": 7, "org_id": 5, "title": "右江区委常委、宣传部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名未知"},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 政法委书记
    {"person_id": 8, "org_id": 6, "title": "右江区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名未知"},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
]

# ═══════════════════════════════════════════════════════════════
# 4. RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════

relationships = [
    # 党政正职搭档关系（均待查）
    {
        "person_a": 1, "person_b": 2,
        "type": "党政正职搭档",
        "context": "右江区委书记与区长——工作搭档关系，姓名均待查",
        "overlap_org": "右江区四套班子",
        "overlap_period": "",
        "source": "GAP",
        "confidence": "unverified",
    },
    # 区委书记与副书记
    {
        "person_a": 1, "person_b": 3,
        "type": "上下级",
        "context": "区委书记与区委副书记——常委会共事关系",
        "overlap_org": "右江区委常委会",
        "overlap_period": "",
        "source": "GAP",
        "confidence": "unverified",
    },
    # 区长与常务副区长
    {
        "person_a": 2, "person_b": 4,
        "type": "上下级",
        "context": "区长与常务副区长——政府领导班子",
        "overlap_org": "右江区人民政府",
        "overlap_period": "",
        "source": "GAP",
        "confidence": "unverified",
    },
    # 纪委书记与区委书记
    {
        "person_a": 1, "person_b": 5,
        "type": "监督关系",
        "context": "党委与纪委——全面从严治党主体责任和监督责任",
        "overlap_org": "右江区委常委会",
        "overlap_period": "",
        "source": "GAP",
        "confidence": "unverified",
    },
]

# ═══════════════════════════════════════════════════════════════
# 5. BUILD
# ═══════════════════════════════════════════════════════════════

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
    print(f"Build complete: {DB_PATH}, {GEXF_PATH}")
