#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
盐田区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 深圳市
Region: 盐田区
Targets: 区委书记 & 区长

Research Sources:
- 深圳盐田政府在线 (yantian.gov.cn) — 政务动态报道确认区委书记李忠、区长邓飞波在任
- 维基百科 (zh.wikipedia.org) — 盐田区词条（邓飞波标注信息有误，Wikipedia编辑滞后）
- 深圳盐田政府在线 — 区委常委会、区政府会议新闻报道确认领导班子成员
- 南方日报/深圳特区报 — 相关人事报道

Research Date: 2026-07-22
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = '盐田区'
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DATABASE_DIR, f'{SLUG}_network.db')
GEXF_PATH = os.path.join(GRAPH_DIR, f'{SLUG}_network.gexf')

# The script uses gov_relation.runner (which internally uses sqlite3)
import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    {
        'id': 1,
        'name': '李忠',
        'gender': '男',
        'ethnicity': '汉族',
        'birth': '待查',
        'birthplace': '待查',
        'native_place': '待查',
        'education': '待查',
        'party_join': '中共党员',
        'work_start': '待查',
        'current_post': '盐田区委书记',
        'current_org': '中共深圳市盐田区委员会',
        'source': '深圳盐田政府在线: 2026年7月多篇区委常委会新闻报道确认李忠以区委书记身份主持会议'
    },
    {
        'id': 2,
        'name': '邓飞波',
        'gender': '男',
        'ethnicity': '汉族',
        'birth': '待查',
        'birthplace': '待查',
        'native_place': '待查',
        'education': '待查',
        'party_join': '中共党员',
        'work_start': '待查',
        'current_post': '盐田区委副书记、区长',
        'current_org': '盐田区人民政府',
        'source': '深圳盐田政府在线: 2026年7月8日报道确认邓飞波以区委副书记、区长身份主持区政府会议'
    },
    {
        'id': 3,
        'name': '乔宏彬',
        'gender': '男',
        'ethnicity': '汉族',
        'birth': '待查',
        'birthplace': '待查',
        'native_place': '待查',
        'education': '待查',
        'party_join': '中共党员',
        'work_start': '待查',
        'current_post': '盐田区人大常委会主任',
        'current_org': '深圳市盐田区人民代表大会常务委员会',
        'source': '深圳盐田政府在线: 2026年7月3日两优一先表彰大会报道确认乔宏彬以区人大常委会主任身份出席'
    },
    {
        'id': 4,
        'name': '尹书彬',
        'gender': '男',
        'ethnicity': '汉族',
        'birth': '待查',
        'birthplace': '待查',
        'native_place': '待查',
        'education': '待查',
        'party_join': '中共党员',
        'work_start': '待查',
        'current_post': '盐田区政协主席',
        'current_org': '中国人民政治协商会议深圳市盐田区委员会',
        'source': '深圳盐田政府在线: 2026年7月3日两优一先表彰大会报道确认尹书彬以区政协主席身份出席'
    },
    {
        'id': 5,
        'name': '曾红英',
        'gender': '女',
        'ethnicity': '汉族',
        'birth': '待查',
        'birthplace': '待查',
        'native_place': '待查',
        'education': '待查',
        'party_join': '中共党员',
        'work_start': '待查',
        'current_post': '区委常委、组织部部长、党校校长',
        'current_org': '中共深圳市盐田区委组织部',
        'source': '深圳盐田政府在线: 2026年7月3日两优一先表彰大会报道确认曾红英以区委常委、组织部部长身份宣读表彰决定'
    },
]

# 2. Organizations
organizations = [
    {
        'id': 1,
        'name': '中共深圳市盐田区委员会',
        'type': '党委',
        'level': '正处级（区委书记通常高配为副厅级）',
        'parent': '中共深圳市委',
        'location': '深圳市盐田区海山街道深盐路2088号'
    },
    {
        'id': 2,
        'name': '盐田区人民政府',
        'type': '政府',
        'level': '正处级',
        'parent': '深圳市人民政府',
        'location': '深圳市盐田区海山街道深盐路2088号'
    },
    {
        'id': 3,
        'name': '深圳市盐田区人民代表大会常务委员会',
        'type': '人大',
        'level': '正处级',
        'parent': '深圳市人大常委会',
        'location': '深圳市盐田区'
    },
    {
        'id': 4,
        'name': '中国人民政治协商会议深圳市盐田区委员会',
        'type': '政协',
        'level': '正处级',
        'parent': '深圳市政协',
        'location': '深圳市盐田区'
    },
    {
        'id': 5,
        'name': '中共深圳市盐田区委组织部',
        'type': '党委',
        'level': '正处级',
        'parent': '中共深圳市盐田区委员会',
        'location': '深圳市盐田区'
    },
]

# 3. Positions
positions = [
    {'person_id': 1, 'org_id': 1, 'title': '盐田区委书记', 'start': '待查', 'end': '至今', 'rank': '副厅级', 'note': '主持区委全面工作'},
    {'person_id': 2, 'org_id': 1, 'title': '盐田区委副书记', 'start': '待查', 'end': '至今', 'rank': '正处级', 'note': ''},
    {'person_id': 2, 'org_id': 2, 'title': '盐田区区长', 'start': '待查', 'end': '至今', 'rank': '正处级', 'note': '主持区政府全面工作'},
    {'person_id': 3, 'org_id': 3, 'title': '盐田区人大常委会主任', 'start': '待查', 'end': '至今', 'rank': '正处级', 'note': '主持区人大常委会全面工作'},
    {'person_id': 4, 'org_id': 4, 'title': '盐田区政协主席', 'start': '待查', 'end': '至今', 'rank': '正处级', 'note': '主持区政协全面工作'},
    {'person_id': 5, 'org_id': 5, 'title': '组织部部长、党校校长', 'start': '待查', 'end': '至今', 'rank': '正处级', 'note': '兼任区委常委'},
    {'person_id': 5, 'org_id': 1, 'title': '区委常委', 'start': '待查', 'end': '至今', 'rank': '副厅级', 'note': ''},
]

# 4. Relationships
relationships = [
    {
        'person_a': 1,
        'person_b': 2,
        'type': 'superior_subordinate',
        'context': '区委书记与区长：党委与政府主要领导工作搭档关系',
        'strength': 'strong',
        'confidence': 'confirmed',
        'overlap_org': '中共深圳市盐田区委员会/盐田区人民政府',
        'overlap_period': '李忠任区委书记、邓飞波任区长期间',
        'source': '深圳盐田政府在线多篇新闻报道确认'
    },
    {
        'person_a': 1,
        'person_b': 3,
        'type': 'overlap',
        'context': '区委书记与人大主任：区委领导班子与人大主要负责人',
        'strength': 'strong',
        'confidence': 'confirmed',
        'overlap_org': '盐田区',
        'overlap_period': '至今',
        'source': '深圳盐田政府在线: 2026年7月3日两优一先表彰大会报道'
    },
    {
        'person_a': 1,
        'person_b': 4,
        'type': 'overlap',
        'context': '区委书记与政协主席：区委领导班子与政协主要负责人',
        'strength': 'medium',
        'confidence': 'confirmed',
        'overlap_org': '盐田区',
        'overlap_period': '至今',
        'source': '深圳盐田政府在线: 2026年7月3日两优一先表彰大会报道'
    },
    {
        'person_a': 2,
        'person_b': 3,
        'type': 'overlap',
        'context': '区长与人大主任：区政府与人大主要负责人',
        'strength': 'medium',
        'confidence': 'confirmed',
        'overlap_org': '盐田区',
        'overlap_period': '至今',
        'source': '深圳盐田政府在线: 2026年7月3日两优一先表彰大会报道'
    },
    {
        'person_a': 2,
        'person_b': 4,
        'type': 'overlap',
        'context': '区长与政协主席：区政府与政协主要负责人',
        'strength': 'medium',
        'confidence': 'confirmed',
        'overlap_org': '盐田区',
        'overlap_period': '至今',
        'source': '深圳盐田政府在线: 2026年7月3日两优一先表彰大会报道'
    },
    {
        'person_a': 1,
        'person_b': 5,
        'type': 'superior_subordinate',
        'context': '区委书记与组织部部长：党委正职与党委重要部门负责人',
        'strength': 'strong',
        'confidence': 'confirmed',
        'overlap_org': '中共深圳市盐田区委员会',
        'overlap_period': '至今',
        'source': '深圳盐田政府在线: 2026年7月3日两优一先表彰大会报道'
    },
]

# ── Run ──
if __name__ == '__main__':
    print(f'Building {SLUG} network...')
    print(f'  DB: {DB_PATH}')
    print(f'  GEXF: {GEXF_PATH}')
    print(f'  Persons: {len(persons)}')
    print(f'  Organizations: {len(organizations)}')
    print(f'  Positions: {len(positions)}')
    print(f'  Relationships: {len(relationships)}')

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

    print(f'\nDone. Files created:')
    print(f'  - {DB_PATH}')
    print(f'  - {GEXF_PATH}')
