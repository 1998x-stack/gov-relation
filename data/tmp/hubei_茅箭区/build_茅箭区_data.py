#!/usr/bin/env python3
"""十堰市茅箭区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区
调查日期: 2026-07-24
信息来源: 茅箭区人民政府网站 (maojian.shiyan.gov.cn), 十堰市人民政府网站 (shiyan.gov.cn)
备注: 茅箭区是十堰市主城区、城市核心增长极，全国商用车制造产业集群所在地。
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation package is importable
_repo_root = Path(__file__).resolve().parents[3]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "茅箭区"
TODAY = "2026-07-24"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Assistants: org id helpers ───────────────────────────────────────────────
def org_id(base: int) -> int:
    """Offset org IDs into the 100000+ range per runner convention."""
    return base + 100000


# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government, 3xxx = other

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 李琴 — 区委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "李琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茅箭区委书记",
        "current_org": "中共十堰市茅箭区委员会",
        "source": "茅箭区人民政府网站新闻 (maojian.shiyan.gov.cn), 2026年7月"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 何垚辰 — 区委副书记、区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2001,
        "name": "何垚辰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茅箭区委副书记、区长",
        "current_org": "十堰市茅箭区人民政府",
        "source": "十堰市新闻发布会 (shiyan.gov.cn), 2026年7月7日"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 任杰 — 区委副书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "任杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茅箭区委副书记",
        "current_org": "中共十堰市茅箭区委员会",
        "source": "全区'两优一先'表彰大会新闻, 2026年7月1日"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 金菊 — 区人大常委会主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 3001,
        "name": "金菊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茅箭区人大常委会主任",
        "current_org": "十堰市茅箭区人民代表大会常务委员会",
        "source": "全区'两优一先'表彰大会新闻, 2026年7月1日"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 金善朝 — 区政协主席
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 3002,
        "name": "金善朝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茅箭区政协主席",
        "current_org": "中国人民政治协商会议十堰市茅箭区委员会",
        "source": "全区'两优一先'表彰大会新闻, 2026年7月1日"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 董祥吉 — 区委常委、常务副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2002,
        "name": "董祥吉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茅箭区委常委、常务副区长",
        "current_org": "十堰市茅箭区人民政府",
        "source": "十堰市新闻发布会 (shiyan.gov.cn), 2026年7月7日"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 詹峰 — 区委常委、副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2003,
        "name": "詹峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茅箭区委常委、副区长",
        "current_org": "十堰市茅箭区人民政府",
        "source": "何垚辰调研督导重点项目征迁工作新闻, 2026年7月23日"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共十堰市茅箭区委员会", "type": "党委", "level": "县处级", "parent": "中共十堰市委", "location": "十堰市茅箭区"},
    {"id": 2, "name": "十堰市茅箭区人民政府", "type": "政府", "level": "县处级", "parent": "十堰市人民政府", "location": "十堰市茅箭区"},
    {"id": 3, "name": "十堰市茅箭区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "十堰市人大常委会", "location": "十堰市茅箭区"},
    {"id": 4, "name": "中国人民政治协商会议十堰市茅箭区委员会", "type": "政协", "level": "县处级", "parent": "政协十堰市委员会", "location": "十堰市茅箭区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 李琴
    {"person_id": 1001, "org_id": 1, "title": "茅箭区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持区委全面工作"},
    # 何垚辰
    {"person_id": 2001, "org_id": 1, "title": "茅箭区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2001, "org_id": 2, "title": "茅箭区区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持区政府全面工作"},
    # 任杰
    {"person_id": 1002, "org_id": 1, "title": "茅箭区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助书记处理区委日常工作"},
    # 金菊
    {"person_id": 3001, "org_id": 3, "title": "茅箭区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 金善朝
    {"person_id": 3002, "org_id": 4, "title": "茅箭区政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 董祥吉
    {"person_id": 2002, "org_id": 2, "title": "茅箭区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责区政府常务工作"},
    {"person_id": 2002, "org_id": 1, "title": "茅箭区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 詹峰
    {"person_id": 2003, "org_id": 2, "title": "茅箭区委常委、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2003, "org_id": 1, "title": "茅箭区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 李琴 — 何垚辰：党政一把手
    {"person_a": 1001, "person_b": 2001, "type": "党政搭档", "context": "区委书记与区长",
     "overlap_org": "中共茅箭区委/茅箭区人民政府", "overlap_period": "2026年"},
    # 李琴 — 任杰：书记与副书记
    {"person_a": 1001, "person_b": 1002, "type": "上下级", "context": "区委书记与区委副书记",
     "overlap_org": "中共茅箭区委", "overlap_period": "2026年"},
    # 何垚辰 — 董祥吉：区长与常务副区长
    {"person_a": 2001, "person_b": 2002, "type": "上下级", "context": "区长与常务副区长",
     "overlap_org": "茅箭区人民政府", "overlap_period": "2026年"},
    # 何垚辰 — 詹峰：区长与副区长
    {"person_a": 2001, "person_b": 2003, "type": "上下级", "context": "区长与副区长",
     "overlap_org": "茅箭区人民政府", "overlap_period": "2026年"},
    # 李琴 — 金菊：党委与人大
    {"person_a": 1001, "person_b": 3001, "type": "党委与人大", "context": "区委书记与人大常委会主任",
     "overlap_org": "茅箭区", "overlap_period": "2026年"},
    # 李琴 — 金善朝：党委与政协
    {"person_a": 1001, "person_b": 3002, "type": "党委与政协", "context": "区委书记与政协主席",
     "overlap_org": "茅箭区", "overlap_period": "2026年"},
    # 董祥吉 — 詹峰：同为副区长
    {"person_a": 2002, "person_b": 2003, "type": "同僚", "context": "常务副区长与副区长",
     "overlap_org": "茅箭区人民政府", "overlap_period": "2026年"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD & RUN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 茅箭区人民政府网站 (maojian.shiyan.gov.cn)")
    print("=" * 60)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print()
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")
