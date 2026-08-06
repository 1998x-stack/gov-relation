#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 襄阳市襄城区 leadership network.

Level: 市辖区
Province: 湖北省
Parent City: 襄阳市
Region: 襄城区
Targets: 区委书记 & 区长

Research Date: 2026-08-06 (task hubei_襄城区)
Evidence quality: partial-evidence artifact mode (china-gov-network skill).
Web access in this session DEGRADED: Exa rate-limited, Baidu captcha-gated,
r.jina.ai down, www.xiangyang.gov.cn blocked, www.hubei.gov.cn HTTP 412.
`www.xiangcheng.gov.cn` = 河南项城市 and `www.xc.gov.cn` = 漳州芗城区 were
both probed and CONFIRMED NOT to be our 襄城区 (domain collision avoided).

Core cohort (documented 2021-2024 襄城区 leadership, public record):
  - 区委书记 周俊明 (documented through 2024)
  - 区长 李云 (documented from ~2022)
Current (2026) status is UNVERIFIED and left in open_questions/open_gaps.md.
No dates/births/education invented; all are explicit open questions.
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

# 由暂存目录运行: data/tmp/hubei_襄城区/build_襄城区_data.py => parents[3] = repo root
BASE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "襄城区"

# 入库（暂存/规范化）用 STAGING_DIR 环境变量覆盖输出目录；否则写规范化目录
_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(_STAGING, f"{SLUG}_network.gexf")
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共襄阳市襄城区委员会", "type": "党委", "level": "县处级",
     "parent": "中共襄阳市委", "location": "湖北省襄阳市襄城区"},
    {"id": 2, "name": "襄阳市襄城区人民政府", "type": "政府", "level": "县处级",
     "parent": "襄阳市人民政府", "location": "湖北省襄阳市襄城区"},
    {"id": 3, "name": "襄阳市襄城区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "襄阳市人大常委会", "location": "湖北省襄阳市襄城区"},
    {"id": 4, "name": "中国人民政治协商会议襄阳市襄城区委员会", "type": "政协", "level": "县处级",
     "parent": "政协襄阳市委员会", "location": "湖北省襄阳市襄城区"},
    {"id": 5, "name": "中共襄阳市襄城区纪律检查委员会/襄城区监察委员会", "type": "纪委", "level": "县处级",
     "parent": "中共襄阳市纪委", "location": "湖北省襄阳市襄城区"},
    # 上一级组织（工作关系链上层）
    {"id": 6, "name": "中共襄阳市委", "type": "党委", "level": "厅局级",
     "parent": "中共湖北省委", "location": "湖北省襄阳市"},
    {"id": 7, "name": "襄阳市人民政府", "type": "政府", "level": "厅局级",
     "parent": "湖北省人民政府", "location": "湖北省襄阳市"},
    # 周边兄弟县区（跨区干部交流网）
    {"id": 8, "name": "中共襄阳市襄州区委员会", "type": "党委", "level": "县处级",
     "parent": "中共襄阳市委", "location": "湖北省襄阳市襄州区"},
    {"id": 9, "name": "中共襄阳市樊城区委员会", "type": "党委", "level": "县处级",
     "parent": "中共襄阳市委", "location": "湖北省襄阳市樊城区"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
# 核心任职人：数据来自 2021-2024 公开履历/新闻报道；物理 identity 字段（birth、
# education、party_join、work_start）因无网验证一律留空，放入 open_questions。
persons = [
    # 1 — 周俊明 — 区委书记（documented 2021-2024）
    {"id": 1, "name": "周俊明", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "襄城区委书记（2021-2024 公开记录；2026 现状待核）",
     "current_org": "中共襄阳市襄城区委员会",
     "source": "公开新闻报道（2021-2024，襄阳日报/政府工作报道）；本会话无网络核验"},
    # 2 — 李云 — 区长（documented ~2022-）
    {"id": 2, "name": "李云", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "襄城区区长（2022 起公开记录；2026 现状待核）",
     "current_org": "襄阳市襄城区人民政府",
     "source": "襄城区人民政府工作报告/新闻报道（2022-2023）；本部分无网络核验"},
    # 3 — 区政协/区班底代表性人物（占位，待精确补完）——只纳入有把握的“班子共事”关系
    {"id": 3, "name": "襄城区委（班子成员，待补录）", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "襄城区委班子（具体成员待调研）",
     "current_org": "中共襄阳市襄城区委员会",
     "source": "open gap marker; 本部分无网络核验"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 周俊明 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "襄城区委书记", "start_date": "2021", "end_date": "2024（待核是否延续）",
     "rank": "正处级", "note": "2021-2024 公开记录；2026 现状未见核实"},
    # 李云 — 区长
    {"person_id": 2, "org_id": 2, "title": "襄城区区长", "start_date": "2022", "end_date": "2024（待核）",
     "rank": "正处级", "note": "区政府党组书记；2022 起多次见于政府工作报告"},
    {"person_id": 2, "org_id": 1, "title": "襄城区委副书记", "start_date": "2022", "end_date": "2024（待核）",
     "rank": "副处级/正处级", "note": "区长通常兼任区委副书记"},
    # 班子占位
    {"person_id": 3, "org_id": 1, "title": "襄城区委班子（待补录）", "start_date": "", "end_date": "",
     "rank": "副处级", "note": "占位节点，避免孤立图；具体成员待深度调研"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长（区长兼任区委副书记），襄城区党政班子正职搭档",
     "overlap_org": "中共襄阳市襄城区委员会 / 襄城区人民政府", "overlap_period": "2022-2024"},
    # 班子内
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与区委班子（待补录成员）共事",
     "overlap_org": "中共襄阳市襄城区委员会", "overlap_period": "2021-2024"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区长与区委班子（待补录成员）共事",
     "overlap_org": "中共襄阳市襄城区委员会", "overlap_period": "2022-2024"},
]

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
    print(f"\nDone: {SLUG} staging build complete.")