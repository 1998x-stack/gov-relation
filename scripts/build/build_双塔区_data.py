#!/usr/bin/env python3
"""
辽宁省朝阳市双塔区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Shuangta District leadership.

Level: 市辖区 (县处级)
Province: 辽宁省
Parent City: 朝阳市
Targets: 区委书记 & 区长

Sources:
- Baidu AI search aggregated results (高飞简历, 宋家宝简历) — accessed 2026-07-25
- 双塔区人民政府办公室领导分工通知（政府文件片段）
- 双塔区第九次党代会报道

Note: Official site shuangta.gov.cn was not directly accessible.
"""

import sqlite3  # noqa: used indirectly via gov_relation.runner
import sys
import os
from pathlib import Path

# Ensure gov_relation is importable
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]  # data/tmp/<task_id>/ -> data/ -> repo root
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ════════════════════════════════════════════
# SLUG
# ════════════════════════════════════════════
SLUG = "双塔区"

# ════════════════════════════════════════════
# PATHS (staging: updated by process_tmp.py on promotion)
# ════════════════════════════════════════════
DB_PATH = SCRIPT_DIR / f"{SLUG}_network.db"
GEXF_PATH = SCRIPT_DIR / f"{SLUG}_network.gexf"

# ════════════════════════════════════════════
# PERSONS
# ════════════════════════════════════════════
persons = [
    # ── 区委书记 (Party Secretary): 高飞 ──
    {
        "id": 1,
        "name": "高飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "辽宁鞍山（推测）",
        "education": "在职大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共朝阳市双塔区委员会",
        "source": "百度聚合搜索（鞍山市水利局履历+任前公示+双塔区调研报道）",
    },
    # ── 区委副书记、区长 (District Mayor): 宋家宝 ──
    {
        "id": 2,
        "name": "宋家宝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "朝阳市双塔区人民政府",
        "source": "百度聚合搜索（省工信厅+瓦房店挂职+双塔区代区长）",
    },
    # ── 区委常委、常务副区长: 王帅 (推测为常务副区长) ──
    {
        "id": 3,
        "name": "王帅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "朝阳市双塔区人民政府",
        "source": "双塔区政府办领导分工通知；大凌河流域区级河长信息",
    },
    # ── 区委常委、副区长: 王宝生（兼经开区职务） ──
    {
        "id": 10,
        "name": "王宝生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "朝阳市双塔区人民政府/朝阳经济技术开发区",
        "source": "双塔区政府办领导分工通知；双塔区党代会报道",
    },
    # ── 区委常委、副区长: 袁满 ──
    {
        "id": 11,
        "name": "袁满",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "朝阳市双塔区人民政府",
        "source": "双塔区政府办领导分工通知",
    },
    # ── 区委常委、副区长: 成锋 ──
    {
        "id": 12,
        "name": "成锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "朝阳市双塔区人民政府",
        "source": "广东省河北商会调研报道（双塔区委书记高飞带队，成锋同行）",
    },
    # ── 区委常委、组织部部长: 刘永新 ──
    {
        "id": 5,
        "name": "刘永新",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共朝阳市双塔区委组织部",
        "source": "百度搜索摘要（刘永新：区委常委、组织部部长）",
    },
    # ── 副区长、市公安局北塔分局局长: 张德宝 ──
    {
        "id": 8,
        "name": "张德宝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、市公安局北塔分局局长",
        "current_org": "朝阳市双塔区人民政府/朝阳市公安局北塔分局",
        "source": "双塔区政府办领导分工通知",
    },
    # ── 副区长: 刘兴璐 ──
    {
        "id": 13,
        "name": "刘兴璐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "朝阳市双塔区人民政府",
        "source": "双塔区政府办领导分工通知",
    },
    # ── 副区长: 王跃飞 ──
    {
        "id": 14,
        "name": "王跃飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "朝阳市双塔区人民政府",
        "source": "双塔区政府办领导分工通知",
    },
    # ── 副区长: 陈天虹 ──
    {
        "id": 15,
        "name": "陈天虹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "朝阳市双塔区人民政府",
        "source": "双塔区政府办领导分工通知",
    },
]

# ════════════════════════════════════════════
# ORGANIZATIONS
# ════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共朝阳市双塔区委员会", "type": "党委", "level": "县处级", "parent": "中共朝阳市委员会", "location": "辽宁省朝阳市双塔区"},
    {"id": 2, "name": "朝阳市双塔区人民政府", "type": "政府", "level": "县处级", "parent": "朝阳市人民政府", "location": "辽宁省朝阳市双塔区"},
    {"id": 3, "name": "中共朝阳市双塔区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共朝阳市双塔区委员会", "location": "辽宁省朝阳市双塔区"},
    {"id": 4, "name": "朝阳市双塔区监察委员会", "type": "监察", "level": "县处级", "parent": "朝阳市双塔区人民代表大会", "location": "辽宁省朝阳市双塔区"},
    {"id": 5, "name": "中共朝阳市双塔区委组织部", "type": "党委", "level": "乡科级", "parent": "中共朝阳市双塔区委员会", "location": "辽宁省朝阳市双塔区"},
    {"id": 6, "name": "中共朝阳市双塔区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共朝阳市双塔区委员会", "location": "辽宁省朝阳市双塔区"},
    {"id": 7, "name": "中共朝阳市双塔区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共朝阳市双塔区委员会", "location": "辽宁省朝阳市双塔区"},
    {"id": 8, "name": "朝阳市双塔区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "朝阳市人民代表大会常务委员会", "location": "辽宁省朝阳市双塔区"},
    {"id": 9, "name": "中国人民政治协商会议朝阳市双塔区委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议朝阳市委员会", "location": "辽宁省朝阳市双塔区"},
    {"id": 10, "name": "朝阳经济技术开发区", "type": "开发区", "level": "县处级", "parent": "朝阳市人民政府", "location": "辽宁省朝阳市双塔区"},
    {"id": 11, "name": "朝阳市公安局北塔分局", "type": "政府", "level": "乡科级", "parent": "朝阳市公安局", "location": "辽宁省朝阳市双塔区"},
]

# ════════════════════════════════════════════
# POSITIONS
# ════════════════════════════════════════════
positions = [
    # 高飞 in 区委/人武部
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026年（待确认月份）", "end_date": "present", "rank": "正处级", "note": "双塔区区委书记，来自鞍山市水利局"},
    # 宋家宝 in 区政府
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "来自省工信厅/瓦房店市"},
    # 王帅 in 区政府
    {"person_id": 3, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼大凌河流域区级河长"},
    # 王宝生 in 区政府/经开区
    {"person_id": 10, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 10, "title": "朝阳经济技术开发区党工委副书记、管委会常务副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 袁满 in 区政府
    {"person_id": 11, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 成锋 in 区政府
    {"person_id": 12, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘永新 in 组织部
    {"person_id": 5, "org_id": 5, "title": "区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张德宝 in 区政府/公安局
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 11, "title": "市公安局北塔分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘兴璐 in 区政府
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王跃飞 in 区政府
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈天虹 in 区政府
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ════════════════════════════════════════════
# RELATIONSHIPS
# ════════════════════════════════════════════
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长，党政主要负责人", "overlap_org": "中共朝阳市双塔区委员会/朝阳市双塔区人民政府", "overlap_period": "至今"},
    # 书记—副区长们（区委常委关系）
    {"person_a": 1, "person_b": 3, "type": "领导", "context": "区委书记—区委常委、副区长", "overlap_org": "中共朝阳市双塔区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "领导", "context": "区委书记—区委常委、副区长", "overlap_org": "中共朝阳市双塔区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "领导", "context": "区委书记—区委常委、副区长", "overlap_org": "中共朝阳市双塔区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "领导", "context": "区委书记—区委常委、副区长", "overlap_org": "中共朝阳市双塔区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "领导", "context": "区委书记领导组织工作", "overlap_org": "中共朝阳市双塔区委员会", "overlap_period": ""},
    # 区长—副区长们（政府班子）
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—区委常委、副区长", "overlap_org": "朝阳市双塔区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—副区长（兼公安局长）", "overlap_org": "朝阳市双塔区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "区长—副区长", "overlap_org": "朝阳市双塔区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "区长—副区长", "overlap_org": "朝阳市双塔区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "区长—副区长", "overlap_org": "朝阳市双塔区人民政府", "overlap_period": ""},
    # 王宝生兼任经开区职务
    {"person_a": 10, "person_b": 10, "type": "兼任", "context": "区委常委、副区长兼经开区党工委副书记、管委会常务副主任", "overlap_org": "朝阳经济技术开发区", "overlap_period": ""},
    # 张德宝兼任公安局长
    {"person_a": 8, "person_b": 8, "type": "兼任", "context": "副区长兼市公安局北塔分局局长", "overlap_org": "朝阳市公安局北塔分局", "overlap_period": ""},
]

# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════
if __name__ == "__main__":
    print(f"Building {SLUG} leadership network...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"[OK] DB: {DB_PATH}")
    print(f"[OK] GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
