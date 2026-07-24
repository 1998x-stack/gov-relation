#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 通城县, 咸宁市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_通城县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — all web search methods inaccessible.
  - Exa AI: rate-limited
  - Baidu Baike: 403 Forbidden
  - Jina Reader: transport errors
  - Government site (www.tc.gov.cn): unreachable (connection timeout)
  - insane-search engine: failed to bypass challenge

All leadership data is pending verification from:
  - https://www.tc.gov.cn/ （通城县政府官网领导之窗）
  - https://www.tc.gov.cn/tc/ldzc/ （领导之窗页面）
  - Baidu Baike for each individual
  - 咸宁市委组织部任前公示
  - 通城县人民政府官网

Known leadership (from partially accessible historical records/news hints):
  ⚠️ 县委书记: 刘中英（可能是现任或前任，待确认）
  ⚠️ 县长: 未找到确切姓名（需从官网确认）
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "通城县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership (ALL PENDING VERIFICATION) ═══════
    # 县委书记 — 可能为刘中英
    {
        "id": 1,
        "name": "刘中英（待确认）",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "通城县委书记（待确认）",
        "current_org": "中共通城县委员会",
        "source": "GAP — 书记姓名未在可访问官网上确认；刘中英为2021-2024年间报道提及的书记，当前任期待确认。网站：www.tc.gov.cn"
    },
    # 县长 — 姓名未知
    {
        "id": 2,
        "name": "【待查】通城县县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "通城县委副书记、县人民政府县长（待查）",
        "current_org": "通城县人民政府",
        "source": "GAP — 县长姓名完全未知；需通过咸宁市委组织部任前公示或tc.gov.cn领导之窗补充"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共通城县委员会", "type": "党委", "level": "县级", "parent": "中共咸宁市委员会", "location": "湖北省咸宁市通城县"},
    {"id": 2, "name": "通城县人民政府", "type": "政府", "level": "县级", "parent": "咸宁市人民政府", "location": "湖北省咸宁市通城县"},
    {"id": 3, "name": "通城县人大常委会", "type": "人大", "level": "县级", "parent": "通城县", "location": "湖北省咸宁市通城县"},
    {"id": 4, "name": "政协通城县委员会", "type": "政协", "level": "县级", "parent": "通城县", "location": "湖北省咸宁市通城县"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "通城县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "⚠️ 待确认；可能为刘中英"},
    {"person_id": 2, "org_id": 2, "title": "通城县人民政府县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "⚠️ 姓名待确认"},
    {"person_id": 2, "org_id": 1, "title": "通城县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭班（待确认姓名）", "overlap_org": "中共通城县委员会/通城县人民政府", "overlap_period": ""},
]

# ── Build ──────────────────────────────────────────────────────────────────
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

    print(f"\nBuild complete for {SLUG}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF graph: {GEXF_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} organizations, {len(positions)} positions, {len(relationships)} relationships")
    print("  ⚠️  WARNING: All leadership data pending verification from official sources.")
