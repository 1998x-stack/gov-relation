#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
源城区领导班子工作关系网络 — 数据构建脚本 (staging)
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 河源市
Region: 源城区
Targets: 区委书记 & 区长

Research Sources:
- 源城区人民政府门户网站 (www.gdyc.gov.cn) — 领导之窗
- 百度百科
- 南方都市报 (2023年11月关于曾宪旺跨市调动的报道)

Current status (as of 2026-07-22):
- 区委书记: 曾宪旺（跨市调动，原深圳福田区委常委）
- 区长: 邓勇（区委副书记，区政府党组书记、区长，一级调研员）
- 区人大常委会主任: 刘贞华
- 区政协主席: 黄小华

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "源城区"
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
        "name": "曾宪旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年6月",
        "birthplace": "湖南宜章",
        "native_place": "湖南宜章",
        "education": "大学（文学学士）",
        "party_join": "中共党员",
        "work_start": "1997年7月",
        "current_post": "中共河源市源城区委书记",
        "current_org": "中共河源市源城区委员会",
        "source": "百度百科:曾宪旺; 南方都市报2023-11-29:福田区委常委曾宪旺跨市调动任源城区委书记; 源城区人民政府门户网站"
    },
    {
        "id": 2,
        "name": "邓勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职硕士研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共河源市源城区委副书记、区政府党组书记、区长",
        "current_org": "河源市源城区人民政府",
        "source": "源城区人民政府门户网站:领导之窗(www.gdyc.gov.cn); 百度百科:邓勇"
    },
    # ════════════════════════════════════════
    # 区人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "刘贞华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "河源市源城区人大常委会主任",
        "current_org": "河源市源城区人民代表大会常务委员会",
        "source": "源城区人民政府门户网站:2025-02-14会议新闻"
    },
    # ════════════════════════════════════════
    # 区政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "黄小华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中国人民政治协商会议河源市源城区委员会主席",
        "current_org": "中国人民政治协商会议河源市源城区委员会",
        "source": "源城区人民政府门户网站:2025-02-14会议新闻"
    },
    # ════════════════════════════════════════
    # 区政府领导（源城区人民政府门户网站领导之窗）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "蓝锦建",
        "gender": "男",
        "ethnicity": "畲族",
        "birth": "1974年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "源城区委常委、区政府党组成员、副区长",
        "current_org": "河源市源城区人民政府",
        "source": "源城区人民政府门户网站:领导之窗"
    },
    {
        "id": 6,
        "name": "王启军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "源城区委常委、区政府副区长",
        "current_org": "河源市源城区人民政府",
        "source": "源城区人民政府门户网站:领导之窗"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "孙锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（已离任源城区，曾任源城区委书记）",
        "current_org": "（已离任）",
        "source": "源城区人民政府门户网站:历史新闻"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共河源市源城区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共河源市委员会",
        "location": "河源市源城区"
    },
    {
        "id": 2,
        "name": "河源市源城区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "河源市人民政府",
        "location": "河源市源城区"
    },
    {
        "id": 3,
        "name": "河源市源城区人民代表大会常务委员会",
        "type": "人大",
        "level": "市辖区",
        "parent": "河源市人民代表大会常务委员会",
        "location": "河源市源城区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议河源市源城区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "中国人民政治协商会议河源市委员会",
        "location": "河源市源城区"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 曾宪旺（现任区委书记）
    {"person_id": 1, "org_id": 1, "title": "中共河源市源城区委书记", "start": "2023-11", "end": "present", "rank": "正处级", "note": "曾宪旺2023年11月从深圳福田区委常委跨市调任源城区委书记"},
    # 曾宪旺在深圳的履历
    {"person_id": 1, "org_id": 2, "title": "深圳市龙岗区委常委、区委(府)办主任、区委教育工委书记", "start": "2021-09", "end": "2022", "rank": "副厅级", "note": "龙岗区委换届当选常委"},
    {"person_id": 1, "org_id": 2, "title": "深圳市福田区委常委", "start": "2022", "end": "2023-11", "rank": "副厅级", "note": "跨区调动任福田区委常委"},
    # 邓勇（现任区长）
    {"person_id": 2, "org_id": 2, "title": "河源市源城区区长", "start": "待查", "end": "present", "rank": "正处级", "note": "区政府党组书记、区长，一级调研员"},
    {"person_id": 2, "org_id": 1, "title": "中共河源市源城区委副书记", "start": "待查", "end": "present", "rank": "正处级", "note": "区委副书记兼区长"},
    # 刘贞华（人大常委会主任）
    {"person_id": 3, "org_id": 3, "title": "河源市源城区人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 黄小华（政协主席）
    {"person_id": 4, "org_id": 4, "title": "政协河源市源城区委员会主席", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 蓝锦建（区委常委、副区长）
    {"person_id": 5, "org_id": 2, "title": "源城区委常委、副区长", "start": "待查", "end": "present", "rank": "副处级", "note": "区政府党组成员；分管住建、城管、自然资源"},
    {"person_id": 5, "org_id": 1, "title": "中共河源市源城区委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 王启军（区委常委、副区长）
    {"person_id": 6, "org_id": 2, "title": "源城区委常委、副区长", "start": "待查", "end": "present", "rank": "副处级", "note": "分管科技、工信、商务、招商引资"},
    {"person_id": 6, "org_id": 1, "title": "中共河源市源城区委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 孙锋（前任区委书记）
    {"person_id": 7, "org_id": 1, "title": "中共河源市源城区委书记", "start": "待查", "end": "2023-11", "rank": "正处级", "note": "孙锋离任后由曾宪旺接任"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记曾宪旺与区长邓勇是源城区最重要的党政搭档", "overlap_org": "中共河源市源城区委员会/河源市源城区人民政府", "overlap_period": "2023-11至今"},
    # 前后任区委书记
    {"person_a": 7, "person_b": 1, "type": "前后任", "context": "孙锋（?至2023-11）→曾宪旺（2023-11至今）", "overlap_org": "中共河源市源城区委员会", "overlap_period": "2023-11交接"},
    # 区委常委班子内部
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "蓝锦建为区委常委、副区长，在区委书记领导下工作", "overlap_org": "中共河源市源城区委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "王启军为区委常委、副区长，在区委书记领导下工作", "overlap_org": "中共河源市源城区委员会", "overlap_period": "当前"},
    # 区政府班子内部
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "蓝锦建作为副区长协助区长邓勇工作", "overlap_org": "河源市源城区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "王启军作为副区长协助区长邓勇工作", "overlap_org": "河源市源城区人民政府", "overlap_period": "当前"},
    # 人大与区委
    {"person_a": 1, "person_b": 3, "type": "党政关系", "context": "区人大常委会主任刘贞华与区委书记曾宪旺的党政协作", "overlap_org": "源城区领导班子", "overlap_period": "当前"},
    # 政协与区委
    {"person_a": 1, "person_b": 4, "type": "党政关系", "context": "区政协主席黄小华与区委书记曾宪旺的党政协作", "overlap_org": "源城区领导班子", "overlap_period": "当前"},
]


# ── Build ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")
