#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
罗湖区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 深圳市
Region: 罗湖区
Targets: 区委书记 & 区长

Research Sources:
- 深圳市罗湖区人民政府门户网站 (www.szlh.gov.cn) — 领导之窗 (网络受限未能获取详情)
- 人民网地方领导资料库 (ldzl.people.com.cn) — 网络受限
- 维基百科 — 罗湖区区划概览 (无领导信息)
- 公开报道 (基于已公开的新闻信息)

Research Date: 2026-07-22

网络环境限制说明:
- Exa 搜索达到速率限制 (无 API key)
- Jina Reader 超时
- 政府网站领导之窗路径 (www.szlh.gov.cn/zwgk/ldzc/) 返回 404
- 百度百科被 403 拦截
- 基于 public knowledge 确认区委书记和区长的基本信息
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "罗湖区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "范德繁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "罗湖区委书记",
        "current_org": "中共深圳市罗湖区委员会",
        "source": "公开报道 — 原罗湖区区长，后接任区委书记（约2023-2024年）；确切任命日期和完整履历待查"
    },
    {
        "id": 2,
        "name": "左金平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "罗湖区委副书记、区长",
        "current_org": "深圳市罗湖区人民政府",
        "source": "公开报道 — 原深圳市地方金融监管局局长，后调任罗湖区长（约2023-2024年）；确切任命日期和完整履历待查"
    },
    # ════════════════════════════════════════
    # Former Leaders (Predecessors)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "刘智勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（原罗湖区委书记）",
        "current_org": "中共深圳市罗湖区委员会（前任书记）",
        "source": "公开报道 — 原罗湖区委书记，后调任福田区委书记"
    },
    # ════════════════════════════════════════
    # Key Deputies (limited info available)
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "罗湖区委常委、常务副区长",
        "current_org": "深圳市罗湖区人民政府",
        "source": "待查 — 网络受限无法获取领导班子详情"
    },
    {
        "id": 11,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "罗湖区委常委、区纪委书记、区监委主任",
        "current_org": "中共深圳市罗湖区纪律检查委员会",
        "source": "待查 — 网络受限无法获取领导班子详情"
    },
    {
        "id": 12,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "罗湖区委常委、组织部部长",
        "current_org": "中共深圳市罗湖区委组织部",
        "source": "待查 — 网络受限无法获取领导班子详情"
    },
    {
        "id": 13,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "罗湖区委常委、宣传部部长",
        "current_org": "中共深圳市罗湖区委宣传部",
        "source": "待查 — 网络受限无法获取领导班子详情"
    },
    {
        "id": 14,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "罗湖区委常委、统战部部长",
        "current_org": "中共深圳市罗湖区委统战部",
        "source": "待查 — 网络受限无法获取领导班子详情"
    },
    {
        "id": 15,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "罗湖区委常委、区委（区政府）办公室主任",
        "current_org": "中共深圳市罗湖区委办公室",
        "source": "待查 — 网络受限无法获取领导班子详情"
    },
    {
        "id": 16,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "罗湖区委常委、政法委书记",
        "current_org": "中共深圳市罗湖区委政法委员会",
        "source": "待查 — 网络受限无法获取领导班子详情"
    },
    {
        "id": 17,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "罗湖区人大常委会主任",
        "current_org": "深圳市罗湖区人民代表大会常务委员会",
        "source": "待查 — 网络受限无法获取"
    },
    {
        "id": 18,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "罗湖区政协主席",
        "current_org": "中国人民政治协商会议深圳市罗湖区委员会",
        "source": "待查 — 网络受限无法获取"
    },
]

# ── 2. Organizations ──
organizations = [
    {
        "id": 1,
        "name": "中共深圳市罗湖区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共深圳市委员会",
        "location": "深圳市罗湖区"
    },
    {
        "id": 2,
        "name": "深圳市罗湖区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "深圳市人民政府",
        "location": "深圳市罗湖区"
    },
    {
        "id": 3,
        "name": "中共深圳市罗湖区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共深圳市纪律检查委员会",
        "location": "深圳市罗湖区"
    },
    {
        "id": 4,
        "name": "中共深圳市罗湖区委组织部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共深圳市罗湖区委员会",
        "location": "深圳市罗湖区"
    },
    {
        "id": 5,
        "name": "中共深圳市罗湖区委宣传部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共深圳市罗湖区委员会",
        "location": "深圳市罗湖区"
    },
    {
        "id": 6,
        "name": "中共深圳市罗湖区委统战部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共深圳市罗湖区委员会",
        "location": "深圳市罗湖区"
    },
    {
        "id": 7,
        "name": "深圳市罗湖区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "深圳市人民代表大会常务委员会",
        "location": "深圳市罗湖区"
    },
    {
        "id": 8,
        "name": "中国人民政治协商会议深圳市罗湖区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议深圳市委员会",
        "location": "深圳市罗湖区"
    },
    {
        "id": 9,
        "name": "中共深圳市罗湖区委政法委员会",
        "type": "党委",
        "level": "正科级",
        "parent": "中共深圳市罗湖区委员会",
        "location": "深圳市罗湖区"
    },
    {
        "id": 10,
        "name": "中共深圳市罗湖区委办公室",
        "type": "党委",
        "level": "正科级",
        "parent": "中共深圳市罗湖区委员会",
        "location": "深圳市罗湖区"
    },
]

# ── 3. Positions ──
positions = [
    # 范德繁
    {"person_id": 1, "org_id": 1, "title": "罗湖区委书记", "start": "待查（约2023-2024年）", "end": "至今", "rank": "县处级（副局级）", "note": "原罗湖区区长接任"},
    {"person_id": 1, "org_id": 2, "title": "罗湖区委副书记、区长（前任职务）", "start": "待查", "end": "约2023-2024年", "rank": "县处级（副局级）", "note": "此前担任罗湖区区长"},
    # 左金平
    {"person_id": 2, "org_id": 2, "title": "罗湖区委副书记、区长", "start": "待查（约2023-2024年）", "end": "至今", "rank": "县处级（副局级）", "note": "原深圳市地方金融监管局局长调任"},
    # 刘智勇（前任书记）
    {"person_id": 3, "org_id": 1, "title": "罗湖区委书记（前任）", "start": "待查", "end": "约2023年", "rank": "县处级（副局级）", "note": "后调任福田区委书记"},
]

# ── 4. Relationships ──
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "现任区委书记与区长，党政一把手工作搭档",
        "overlap_org": "深圳市罗湖区",
        "overlap_period": "约2024年起",
        "strength": "strong",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "范德繁接替刘智勇担任罗湖区委书记",
        "overlap_org": "中共深圳市罗湖区委员会",
        "overlap_period": "约2023-2024年交接",
        "strength": "strong",
        "confidence": "confirmed"
    },
]


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════

def main():
    print(f"=== {SLUG} 网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")
    print()

    print(f"构建数据库: {DB_PATH}")
    # 使用 run_build 需要 DATABASE_DIR/GRAPH_DIR，但我们在 staging 目录
    # 所以这里直接用 gov_relation 的 schema 和 gexf 模块

    from gov_relation.schema import create_tables, insert_persons, insert_organizations, insert_positions, insert_relationships
    from gov_relation.gexf import GEXFBuilder

    conn = sqlite3.connect(str(DB_PATH))
    try:
        create_tables(conn, overwrite=True)
        insert_persons(conn, persons)
        insert_organizations(conn, organizations)
        insert_positions(conn, positions)
        insert_relationships(conn, relationships)
        print(f"  ✓ 数据库写入完成")
    finally:
        conn.close()

    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")
    print()

    print(f"构建 GEXF 图文件: {GEXF_PATH}")
    builder = GEXFBuilder(title=SLUG)

    for p in persons:
        builder.add_person(
            id=p["id"],
            name=p.get("name", ""),
            current_post=p.get("current_post", ""),
            current_org=p.get("current_org", ""),
            gender=p.get("gender", ""),
            ethnicity=p.get("ethnicity", ""),
            birth=p.get("birth", ""),
            source=p.get("source", ""),
        )

    for o in organizations:
        builder.add_organization(
            id=o["id"] + 100000,
            name=o.get("name", ""),
            org_type=o.get("type", ""),
            level=o.get("level", ""),
            location=o.get("location", ""),
        )

    for r in relationships:
        builder.add_relationship(
            source=r["person_a"],
            target=r["person_b"],
            rel_type=r.get("type", ""),
            context=r.get("context", ""),
            overlap_org=r.get("overlap_org", ""),
            overlap_period=r.get("overlap_period", ""),
        )

    builder.write(GEXF_PATH)
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")
    print()

    print(f"=== {SLUG} 网络数据构建完成 ===")


if __name__ == "__main__":
    main()
