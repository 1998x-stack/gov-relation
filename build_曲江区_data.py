#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
曲江区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 韶关市
Region: 曲江区
Targets: 区委书记 & 区长

Research Sources:
- 韶关市曲江区人民政府门户网站 (www.qujiang.gov.cn) — 领导之窗/区政府
- 曲江区政府新闻中心 — 区委领导活动报道
- 维基百科 (zh.wikipedia.org) — 曲江区词条

Current status (as of 2026-07-22):
- 区委书记: 宋在军
- 区长: 肖烈南（1981年6月生）
- 常务副区长: 杨文乐（1980年8月生）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "曲江区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 区委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "宋在军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共韶关市曲江区委书记",
        "current_org": "中共韶关市曲江区委员会",
        "source": "曲江区政府新闻中心:2026年多篇报道确认"
    },
    {
        "id": 2,
        "name": "肖烈南",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共韶关市曲江区委副书记、区长",
        "current_org": "曲江区人民政府",
        "source": "曲江区政府领导之窗:http://www.qujiang.gov.cn/zwgk/ldzc/qjqzf/content/post_2033976.html"
    },
    # ════════════════════════════════════════
    # 区政府领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "杨文乐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "公共管理硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、区政府党组副书记、副区长（常务）",
        "current_org": "曲江区人民政府",
        "source": "曲江区政府领导之窗:http://www.qujiang.gov.cn/zwgk/ldzc/qjqzf/content/post_2060109.html"
    },
    {
        "id": 4,
        "name": "杨长虹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、宣传部部长、副区长",
        "current_org": "中共韶关市曲江区委宣传部",
        "source": "曲江区政府领导之窗:http://www.qujiang.gov.cn/zwgk/ldzc/qjqzf/content/post_2764190.html"
    },
    {
        "id": 5,
        "name": "陈焕云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "曲江区人民政府",
        "source": "曲江区政府领导之窗:http://www.qujiang.gov.cn/zwgk/ldzc/qjqzf/content/post_2060168.html"
    },
    {
        "id": 6,
        "name": "刘武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、副区长",
        "current_org": "曲江区人民政府",
        "source": "曲江区政府领导之窗:http://www.qujiang.gov.cn/zwgk/ldzc/qjqzf/content/post_2060184.html"
    },
    {
        "id": 7,
        "name": "戴儒辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "曲江区人民政府",
        "source": "曲江区政府领导之窗:http://www.qujiang.gov.cn/zwgk/ldzc/qjqzf/content/post_2536341.html"
    },
    {
        "id": 8,
        "name": "卢波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "曲江区人民政府",
        "source": "曲江区政府领导之窗:http://www.qujiang.gov.cn/zwgk/ldzc/qjqzf/content/post_2807404.html"
    },
    {
        "id": 9,
        "name": "陈敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "曲江区人民政府",
        "source": "曲江区政府领导之窗:http://www.qujiang.gov.cn/zwgk/ldzc/qjqzf/content/post_2807402.html"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共韶关市曲江区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共韶关市委员会",
        "location": "广东省韶关市曲江区"
    },
    {
        "id": 2,
        "name": "曲江区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "韶关市人民政府",
        "location": "广东省韶关市曲江区"
    },
    {
        "id": 3,
        "name": "中共韶关市曲江区委宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共韶关市曲江区委员会",
        "location": "广东省韶关市曲江区"
    },
    {
        "id": 4,
        "name": "中共韶关市曲江区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共韶关市曲江区委员会",
        "location": "广东省韶关市曲江区"
    },
    {
        "id": 5,
        "name": "曲江区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "韶关市人民代表大会常务委员会",
        "location": "广东省韶关市曲江区"
    },
    {
        "id": 6,
        "name": "中国人民政治协商会议曲江区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "韶关市政协",
        "location": "广东省韶关市曲江区"
    },
    {
        "id": 7,
        "name": "中共韶关市曲江区委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共韶关市曲江区委员会",
        "location": "广东省韶关市曲江区"
    },
    {
        "id": 8,
        "name": "中共韶关市曲江区委政法委员会",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共韶关市曲江区委员会",
        "location": "广东省韶关市曲江区"
    },
]

# 3. Positions
positions = [
    # 宋在军 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "待查", "end": "present", "rank": "县处级正职", "note": "2026年7月仍在任"},
    # 肖烈南 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "待查", "end": "present", "rank": "县处级正职", "note": "1981年6月生，硕士研究生"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 杨文乐 - 常务副区长
    {"person_id": 3, "org_id": 2, "title": "副区长（常务）", "start": "待查", "end": "present", "rank": "县处级副职", "note": "区政府党组副书记"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": "1980年8月生，公共管理硕士"},
    # 杨长虹 - 宣传部长 / 副区长
    {"person_id": 4, "org_id": 3, "title": "宣传部部长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "区委常委"},
    {"person_id": 4, "org_id": 2, "title": "副区长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 陈焕云 - 副区长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 刘武 - 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "区政府党组成员，1981年4月生，工学学士"},
    # 戴儒辉 - 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 卢波 - 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 陈敏 - 副区长
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
]

# 4. Relationships
relationships = [
    # 宋在军 <-> 肖烈南：党政正职搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长党政正职搭档",
        "overlap_org": "中共韶关市曲江区委员会/曲江区人民政府",
        "overlap_period": "2026年（具体起始待查）"
    },
    # 宋在军 <-> 杨文乐
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委/常务副区长的上下级关系",
        "overlap_org": "中共韶关市曲江区委员会",
        "overlap_period": "2026年"
    },
    # 宋在军 <-> 杨长虹
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委/宣传部长的上下级关系",
        "overlap_org": "中共韶关市曲江区委员会",
        "overlap_period": "2026年"
    },
    # 肖烈南 <-> 杨文乐（党政正副职）
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区长与常务副区长的党政正副职搭档",
        "overlap_org": "曲江区人民政府",
        "overlap_period": "2026年"
    },
    # 肖烈南 <-> 各副区长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "曲江区人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "曲江区人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "曲江区人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "曲江区人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "曲江区人民政府", "overlap_period": "2026年"},
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
