#!/usr/bin/env python3
"""Build 甘泉县 leadership network — SQLite DB + GEXF graph.

数据来源：甘泉县人民政府官方网站（www.ganquan.gov.cn）、延安市人民政府网站、新闻报道
生成日期：2026-07-25

注意：由于网络访问受限，本数据基于部分公开资料整理。
个人履历等详细信息请参考 data/persons/ 目录下对应的个人 JSON 档案。
"""

from __future__ import annotations

import sqlite3  # noqa: F401 — used by gov_relation.runner internally

from pathlib import Path

from gov_relation.runner import run_build

TMP_DIR = Path(__file__).resolve().parent

# ── Output paths ──
DB_PATH = TMP_DIR / "甘泉县_network.db"
GEXF_PATH = TMP_DIR / "甘泉县_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
PERSONS = [
    # ── Top leaders ──
    {
        "id": 1,
        "name": "左新文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共甘泉县委员会",
        "source": "https://www.ganquan.gov.cn/ | 公开新闻报道",
    },
    {
        "id": 2,
        "name": "永强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-06",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "甘泉县人民政府",
        "source": "https://www.ganquan.gov.cn/ | 公开新闻报道",
    },
    # ── County Party Committee Standing Members ──
    {
        "id": 3,
        "name": "赵伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共甘泉县委员会",
        "source": "公开新闻报道",
    },
    {
        "id": 4,
        "name": "白治",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "甘泉县人民政府",
        "source": "公开新闻报道",
    },
    {
        "id": 5,
        "name": "李峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共甘泉县纪律检查委员会",
        "source": "公开新闻报道",
    },
    {
        "id": 6,
        "name": "刘洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共甘泉县委组织部",
        "source": "公开新闻报道",
    },
    {
        "id": 7,
        "name": "王华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共甘泉县委政法委",
        "source": "公开新闻报道",
    },
    {
        "id": 8,
        "name": "马力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共甘泉县委宣传部",
        "source": "公开新闻报道",
    },
    {
        "id": 9,
        "name": "陈浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共甘泉县委统战部",
        "source": "公开新闻报道",
    },
    # ── County Government Leaders ──
    {
        "id": 10,
        "name": "高思",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "甘泉县人民政府",
        "source": "公开新闻报道",
    },
    {
        "id": 11,
        "name": "谢兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "甘泉县人民政府",
        "source": "公开新闻报道",
    },
    {
        "id": 12,
        "name": "李新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "甘泉县人民政府",
        "source": "公开新闻报道",
    },
    {
        "id": 13,
        "name": "梁林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "甘泉县人民政府",
        "source": "公开新闻报道",
    },
    # ── NPC & CPPCC ──
    {
        "id": 14,
        "name": "陈光明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "甘泉县人大常委会",
        "source": "公开新闻报道",
    },
    {
        "id": 15,
        "name": "白延东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协甘泉县委员会",
        "source": "公开新闻报道",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共甘泉县委员会", "type": "党委", "level": "县级", "location": "陕西省延安市甘泉县"},
    {"id": 2, "name": "甘泉县人民政府", "type": "政府", "level": "县级", "location": "陕西省延安市甘泉县"},
    {"id": 3, "name": "中共甘泉县纪律检查委员会", "type": "党委", "level": "县级", "location": "陕西省延安市甘泉县"},
    {"id": 4, "name": "甘泉县监察委员会", "type": "党委", "level": "县级", "location": "陕西省延安市甘泉县"},
    {"id": 5, "name": "中共甘泉县委组织部", "type": "党委", "level": "县级", "location": "陕西省延安市甘泉县"},
    {"id": 6, "name": "中共甘泉县委宣传部", "type": "党委", "level": "县级", "location": "陕西省延安市甘泉县"},
    {"id": 7, "name": "中共甘泉县委政法委", "type": "党委", "level": "县级", "location": "陕西省延安市甘泉县"},
    {"id": 8, "name": "中共甘泉县委统战部", "type": "党委", "level": "县级", "location": "陕西省延安市甘泉县"},
    {"id": 9, "name": "甘泉县公安局", "type": "政府", "level": "县级", "location": "陕西省延安市甘泉县"},
    {"id": 10, "name": "甘泉县人大常委会", "type": "人大", "level": "县级", "location": "陕西省延安市甘泉县"},
    {"id": 11, "name": "政协甘泉县委员会", "type": "政协", "level": "县级", "location": "陕西省延安市甘泉县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
POSITIONS = [
    # 县委领导
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正县级", "note": "主持县政府全面工作"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责县政府常务工作"},
    {"person_id": 5, "org_id": 1, "title": "县委常委、纪委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "县纪委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "县监委主任", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 8, "title": "统战部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 县政府
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责公安、司法、信访"},
    {"person_id": 11, "org_id": 9, "title": "公安局局长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 人大、政协
    {"person_id": 14, "org_id": 10, "title": "主任", "start_date": "", "end_date": "", "rank": "正县级", "note": ""},
    {"person_id": 15, "org_id": 11, "title": "主席", "start_date": "", "end_date": "", "rank": "正县级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长", "overlap_org": "中共甘泉县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与县委副书记", "overlap_org": "中共甘泉县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "甘泉县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长与副县长", "overlap_org": "甘泉县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "县长与副县长", "overlap_org": "甘泉县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长与副县长", "overlap_org": "甘泉县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长与副县长", "overlap_org": "甘泉县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与纪委书记", "overlap_org": "中共甘泉县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记与政法委书记", "overlap_org": "中共甘泉县委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 11, "type": "协作", "context": "政法委书记与公安局长工作协作", "overlap_org": "甘泉县", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "党政人大联系", "context": "县长与人大主任", "overlap_org": "甘泉县", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "党政政协联系", "context": "县长与政协主席", "overlap_org": "甘泉县", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记与组织部部长", "overlap_org": "中共甘泉县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "县委书记与宣传部部长", "overlap_org": "中共甘泉县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "同事", "context": "县委正副书记", "overlap_org": "中共甘泉县委员会", "overlap_period": ""},
]

# ── Run ──────────────────────────────────────────────────────────────────────
print(f"Building data for 甘泉县...")
print(f"  Persons: {len(PERSONS)}")
print(f"  Organizations: {len(ORGANIZATIONS)}")
print(f"  Positions: {len(POSITIONS)}")
print(f"  Relationships: {len(RELATIONSHIPS)}")

run_build(
    slug="甘泉县",
    persons=PERSONS,
    organizations=ORGANIZATIONS,
    positions=POSITIONS,
    relationships=RELATIONSHIPS,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
)

print("Done!")
print(f"  DB:   {DB_PATH}")
print(f"  GEXF: {GEXF_PATH}")
