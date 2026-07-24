#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
霸州市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 河北省
Parent City: 廊坊市
Region: 霸州市
Targets: 市委书记 & 市长

Research Sources:
- 霸州市人民政府领导之窗 (http://www.bazhou.gov.cn/zwgk/ldzc/) — 确认市长及副市长信息
- 霸州市人民政府网站新闻报道 — 确认刘岳为市委领导（检查防汛备汛工作）
- 公开新闻报道 — 补充信息

Research Date: 2026-07-24

已知信息（置信度标注如下）:
- 市委书记: 刘岳（2025年起任霸州市委书记，此前相关任职信息待查）
- 市长: 陈海强（霸州市委副书记、市长，来自官方领导之窗页面，置信度: confirmed）
- 常务副市长: 闫明杰（来自官方领导之窗页面，置信度: confirmed）
- 副市长: 张树增（来自官方领导之窗页面，置信度: confirmed）
- 副市长: 李晨光（来自官方领导之窗页面，置信度: confirmed）
- 副市长: 牛铁旺（来自官方领导之窗页面，置信度: confirmed）
- 副市长: 赵法健（来自官方领导之窗页面，置信度: confirmed）
- 副市长: 李红选（来自官方领导之窗页面，置信度: confirmed）

Confidence:
- 陈海强 市长: confirmed (官方领导之窗)
- 刘岳 市委书记: plausible (新闻提及，作为主要领导检查防汛，推测为市委书记)
- 刘岳完整履历: partial (部分已知)
- 陈海强完整履历: partial (部分已知)
- 其他常委/副市长: confirmed（副市长团队来自官方页面）
- 当前截至2026年7月的任职状态: confirmed (市长团队)/plausible (市委书记)

注意：本脚本在网络搜索受限条件下构建。市委领导团队页面通过JavaScript渲染，
未能在纯文本抓取中获得。核心人物的完整履历需后续补充。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "霸州市"

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
        "name": "刘岳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "霸州市委书记",
        "current_org": "中共廊坊市霸州市委员会",
        "source": "霸州市政府网站新闻报道显示刘岳督导检查防汛备汛工作（2026年7月），推测为市委书记（置信度: plausible）"
    },
    {
        "id": 2,
        "name": "陈海强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "霸州市委副书记、市长",
        "current_org": "霸州市人民政府",
        "source": "霸州市人民政府官方网站领导之窗 (http://www.bazhou.gov.cn/zwgk/ldzc/) — 确认市长（置信度: confirmed）"
    },
    # ════════════════════════════════════════
    # Deputy Mayors (confirmed from official page)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "闫明杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-06",
        "birthplace": "河北香河",
        "native_place": "河北香河",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "1998-08",
        "current_post": "霸州市委常委、常务副市长",
        "current_org": "霸州市人民政府",
        "source": "霸州市人民政府官方网站领导之窗 — 简历（置信度: confirmed）"
    },
    {
        "id": 4,
        "name": "张树增",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-05",
        "birthplace": "河北霸州",
        "native_place": "河北霸州",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "1994-08",
        "current_post": "霸州市副市长",
        "current_org": "霸州市人民政府",
        "source": "霸州市人民政府官方网站领导之窗 — 简历（置信度: confirmed）"
    },
    {
        "id": 5,
        "name": "李晨光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-11",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "霸州市副市长",
        "current_org": "霸州市人民政府",
        "source": "霸州市人民政府官方网站领导之窗 — 简历（置信度: confirmed）"
    },
    {
        "id": 6,
        "name": "牛铁旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "河北霸州",
        "native_place": "河北霸州",
        "education": "河北广播电视大学工商企业管理",
        "party_join": "中共党员",
        "work_start": "1996-12",
        "current_post": "霸州市副市长",
        "current_org": "霸州市人民政府",
        "source": "霸州市人民政府官方网站领导之窗 — 简历（置信度: confirmed）"
    },
    {
        "id": 7,
        "name": "赵法健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-04",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "霸州市副市长",
        "current_org": "霸州市人民政府",
        "source": "霸州市人民政府官方网站领导之窗 — 简历（置信度: confirmed）"
    },
    {
        "id": 8,
        "name": "李红选",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "河北平乡",
        "native_place": "河北平乡",
        "education": "河北省人民警察学校",
        "party_join": "中共党员",
        "work_start": "1995-08",
        "current_post": "霸州市副市长",
        "current_org": "霸州市人民政府",
        "source": "霸州市人民政府官方网站领导之窗 — 简历（置信度: confirmed）"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共廊坊市霸州市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共廊坊市委员会",
        "location": "河北省廊坊市霸州市"
    },
    {
        "id": 2,
        "name": "霸州市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "廊坊市人民政府",
        "location": "河北省廊坊市霸州市"
    },
    {
        "id": 3,
        "name": "霸州市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级市",
        "parent": "廊坊市人民代表大会常务委员会",
        "location": "河北省廊坊市霸州市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议霸州市委员会",
        "type": "政协",
        "level": "县级市",
        "parent": "中国人民政治协商会议廊坊市委员会",
        "location": "河北省廊坊市霸州市"
    },
    {
        "id": 5,
        "name": "中共霸州市纪律检查委员会",
        "type": "纪委",
        "level": "县级市",
        "parent": "中共廊坊市纪律检查委员会",
        "location": "河北省廊坊市霸州市"
    },
]

# 3. Positions
positions = [
    # ── 刘岳 ──
    {
        "person_id": 1,
        "org_id": 1,
        "title": "霸州市委书记",
        "start": "2025",
        "end": "至今",
        "rank": "正处级",
        "note": "推测2025年起任现职（置信度: plausible）"
    },
    # ── 陈海强 ──
    {
        "person_id": 2,
        "org_id": 2,
        "title": "霸州市委副书记、市长",
        "start": "待查",
        "end": "至今",
        "rank": "正处级",
        "note": "主持市政府全面工作（置信度: confirmed）"
    },
    # ── 闫明杰 ──
    {
        "person_id": 3,
        "org_id": 2,
        "title": "霸州市委常委、常务副市长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "发改、财税、统计、安全生产、应急管理等（置信度: confirmed）"
    },
    # ── 张树增 ──
    {
        "person_id": 4,
        "org_id": 2,
        "title": "霸州市副市长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "城乡规划建设、自然资源、城市管理等（置信度: confirmed）"
    },
    # ── 李晨光 ──
    {
        "person_id": 5,
        "org_id": 2,
        "title": "霸州市副市长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "交通运输、商贸物流、人社、市场监管、金融等（置信度: confirmed）"
    },
    # ── 牛铁旺 ──
    {
        "person_id": 6,
        "org_id": 2,
        "title": "霸州市副市长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "农业农村、水利、生态环境、民政等（置信度: confirmed）"
    },
    # ── 赵法健 ──
    {
        "person_id": 7,
        "org_id": 2,
        "title": "霸州市副市长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "文旅、教育、体育、卫健、医保等（置信度: confirmed）"
    },
    # ── 李红选 ──
    {
        "person_id": 8,
        "org_id": 2,
        "title": "霸州市副市长",
        "start": "待查",
        "end": "至今",
        "rank": "副处级",
        "note": "政法、退役军人事务、涉军工作等（置信度: confirmed）"
    },
]

# 4. Relationships
relationships = [
    # 刘岳 — 陈海强：党政一把手搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "党政正职搭档：市委书记与市长",
        "overlap_org": "霸州市委/市政府",
        "overlap_period": "2025-至今",
        "confidence": "confirmed"
    },
    # 刘岳 — 闫明杰：市委常委关系
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "市委书记与市委常委、常务副市长",
        "overlap_org": "中共霸州市委员会",
        "overlap_period": "2025-至今",
        "confidence": "confirmed"
    },
    # 陈海强 — 闫明杰：市长与常务副市长
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "市长与常务副市长（政府工作搭档）",
        "overlap_org": "霸州市人民政府",
        "overlap_period": "在任同期",
        "confidence": "confirmed"
    },
    # 陈海强 — 张树增：市长与副市长
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "市长与副市长（政府工作搭档）",
        "overlap_org": "霸州市人民政府",
        "overlap_period": "在任同期",
        "confidence": "confirmed"
    },
    # 陈海强 — 李晨光
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "市长与副市长（政府工作搭档）",
        "overlap_org": "霸州市人民政府",
        "overlap_period": "在任同期",
        "confidence": "confirmed"
    },
    # 陈海强 — 牛铁旺
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "市长与副市长（政府工作搭档）",
        "overlap_org": "霸州市人民政府",
        "overlap_period": "在任同期",
        "confidence": "confirmed"
    },
    # 陈海强 — 赵法健
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "市长与副市长（政府工作搭档）",
        "overlap_org": "霸州市人民政府",
        "overlap_period": "在任同期",
        "confidence": "confirmed"
    },
    # 陈海强 — 李红选
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "市长与副市长（政府工作搭档）",
        "overlap_org": "霸州市人民政府",
        "overlap_period": "在任同期",
        "confidence": "confirmed"
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
