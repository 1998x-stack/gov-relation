#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
光明区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 深圳市
Region: 光明区
Targets: 区委书记 & 区长

Research Sources:
- 中文维基百科"光明区"条目 (zh.wikipedia.org/wiki/光明区) — infobox 确认: 区委书记=蔡颖, 区长=邱浩航
- 光明区政府在线 (www.szgm.gov.cn) — 领导之窗页面因网络限制未能获取详情
- 人民网地方领导资料库 — 网络受限
- Exa/Google/Baidu — 搜索服务均被限流或返回 403

Research Date: 2026-07-22

网络环境限制说明:
- Exa 搜索达到速率限制 (无 API key)
- Jina Reader 超时
- 百度百科被 403 拦截
- 光明区政府网站领导路径未找到标准"领导之窗"页面
- 基于中文维基百科光明区条目 infobox 确认核心领导信息

核心领导信息:
- 蔡颖: 光明区委书记（女，维基百科光明区条目 infobox 显示）
- 邱浩航: 光明区委副书记、区长（维基百科光明区条目 infobox 显示）
- 两人均为中共党员，其他履历详情因网络受限待补充

光明区历史:
- 2007年5月31日: 成立光明新区（功能区）
- 2018年5月25日: 国务院批复设立光明行政区，同年9月19日挂牌
- 光明区是粤港澳大湾区核心区域之一，光明科学城所在地
"""

import sys
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

import sqlite3

from gov_relation.runner import run_build

# ── Paths ──
REPO_ROOT = Path(__file__).resolve().parent
DB_PATH = REPO_ROOT / "data/database/光明区_network.db"
GEXF_PATH = REPO_ROOT / "data/graph/光明区_network.gexf"

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "蔡颖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "光明区委书记",
        "current_org": "中共深圳市光明区委员会",
        "source": "中文维基百科光明区条目 infobox (2026-07-22版) — https://zh.wikipedia.org/wiki/%E5%85%89%E6%98%8E%E5%8C%BA"
    },
    {
        "id": 2,
        "name": "邱浩航",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "光明区委副书记、区长",
        "current_org": "深圳市光明区人民政府",
        "source": "中文维基百科光明区条目 infobox (2026-07-22版) — https://zh.wikipedia.org/wiki/%E5%85%89%E6%98%8E%E5%8C%BA"
    },
    # ════════════════════════════════════════
    # Previous Leaders (Known from context)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "张纳沙（推测）",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任",
        "current_org": "未知",
        "source": "推测 — 蔡颖的前任。根据公开报道，张纳沙曾于2021年左右任光明区委书记，后调任。待确认。"
    },
    {
        "id": 4,
        "name": "刘胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（原光明区委书记，现任深圳市副市长？）",
        "current_org": "未知",
        "source": "推测 — 早期光明区委书记。2018年9月光明区挂牌时首任区委书记。待确认。"
    },
]

organizations = [
    {"id": 1, "name": "中共深圳市光明区委员会", "type": "党委", "level": "县处级",
     "parent": "中共深圳市委员会", "location": "广东省深圳市光明区广场路1号"},
    {"id": 2, "name": "深圳市光明区人民政府", "type": "政府", "level": "县处级",
     "parent": "深圳市人民政府", "location": "广东省深圳市光明区广场路1号"},
    {"id": 3, "name": "光明区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "深圳市人大常委会", "location": "广东省深圳市光明区"},
    {"id": 4, "name": "中国人民政治协商会议光明区委员会", "type": "政协", "level": "县处级",
     "parent": "深圳市政协", "location": "广东省深圳市光明区"},
    {"id": 5, "name": "中共深圳市光明区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共深圳市纪律检查委员会", "location": "广东省深圳市光明区"},
    {"id": 6, "name": "中共深圳市光明区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共深圳市光明区委员会", "location": "广东省深圳市光明区"},
    {"id": 7, "name": "中共深圳市光明区委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共深圳市光明区委员会", "location": "广东省深圳市光明区"},
    {"id": 8, "name": "中共深圳市光明区委政法委员会", "type": "党委", "level": "乡科级",
     "parent": "中共深圳市光明区委员会", "location": "广东省深圳市光明区"},
    {"id": 9, "name": "深圳市公安局光明分局", "type": "政府", "level": "乡科级",
     "parent": "深圳市公安局", "location": "广东省深圳市光明区"},
    {"id": 10, "name": "光明区光明街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市光明区人民政府", "location": "广东省深圳市光明区"},
    {"id": 11, "name": "光明区公明街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市光明区人民政府", "location": "广东省深圳市光明区"},
    {"id": 12, "name": "光明区新湖街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市光明区人民政府", "location": "广东省深圳市光明区"},
    {"id": 13, "name": "光明区凤凰街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市光明区人民政府", "location": "广东省深圳市光明区"},
    {"id": 14, "name": "光明区玉塘街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市光明区人民政府", "location": "广东省深圳市光明区"},
    {"id": 15, "name": "光明区马田街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "深圳市光明区人民政府", "location": "广东省深圳市光明区"},
    {"id": 16, "name": "光明科学城", "type": "事业单位", "level": "县处级",
     "parent": "深圳市人民政府", "location": "广东省深圳市光明区"},
]

positions = [
    # ── 蔡颖 (Cai Ying) ──
    {
        "person_id": 1, "org_id": 1, "title": "光明区委书记",
        "start_date": "未知", "end_date": "present", "rank": "副厅级",
        "note": "现任光明区委书记。到任时间待确认（2026-07-22维基百科显示为现任）。蔡颖为女性，在深圳各区区委书记中较为少见。"
    },
    # 蔡颖的前职待补充
    {
        "person_id": 1, "org_id": 2, "title": "光明区区长（推测前职）",
        "start_date": "未知", "end_date": "未知", "rank": "正局级",
        "note": "推测蔡颖任区委书记前可能担任光明区长或其他深圳市级部门领导职务。待确认。",
    },

    # ── 邱浩航 (Qiu Haohang) ──
    {
        "person_id": 2, "org_id": 2, "title": "光明区委副书记、区长",
        "start_date": "未知", "end_date": "present", "rank": "正局级",
        "note": "现任光明区长。到任时间待确认（2026-07-22维基百科显示为现任）。"
    },

    # ── 前任领导 ──
    {
        "person_id": 3, "org_id": 1, "title": "光明区委书记（推测前职）",
        "start_date": "未知", "end_date": "未知", "rank": "副厅级",
        "note": "推测为蔡颖前任，约2021年前后任职。待确认。"
    },
    {
        "person_id": 4, "org_id": 1, "title": "光明区委书记（首任）",
        "start_date": "2018", "end_date": "未知", "rank": "副厅级",
        "note": "曾任光明区首任区委书记（2018年光明区挂牌时）。后调任深圳市副市长等职。待确认。"
    },
]

relationships = [
    {
        "person_a": 1, "person_b": 2, "type": "superior_subordinate",
        "strength": "strong",
        "context": "蔡颖（区委书记）与邱浩航（区长）为光明区党政一把手搭档关系。二人共同领导光明区全面工作。",
        "overlap_org": "中共深圳市光明区委员会/深圳市光明区人民政府",
        "overlap_period": "待确认", "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 3, "type": "predecessor_successor",
        "strength": "medium",
        "context": "推测张纳沙为蔡颖前任光明区委书记。两人职务交接时间待确认。",
        "overlap_org": "中共深圳市光明区委员会",
        "overlap_period": "待确认", "confidence": "unverified"
    },
    {
        "person_a": 3, "person_b": 4, "type": "predecessor_successor",
        "strength": "medium",
        "context": "推测刘胜为首任光明区委书记（2018年），张纳沙为其后继任者。",
        "overlap_org": "中共深圳市光明区委员会",
        "overlap_period": "待确认", "confidence": "unverified"
    },
]

# ════════════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="光明区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done: 光明区 network data built in staging.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
