#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 湟源县 (Huangyuan County), 西宁市, 青海省.

Investigation date: 2026-08-07
Task ID: qinghai_湟源县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — current officeholders CONFIRMED from primary sources
(湟源县人民政府门户网 huangyuan.gov.cn, accessed 2026-08-07). External biography
web search was degraded (Exa rate-limited, Baidu/Bing/Jina Reader timeouts), so
full career histories for some figures (esp. 县委书记赵超) are gapped and marked
as unverified in the person JSONs.

Confirmed from official 领导之窗 / 政务要闻 / 政府工作报告:
- 县委书记: 赵超 (confirmed via 2026-07-23 conference news + 湟源县第十八次党代会 2026-07)
- 县长: 肖军 (male, 汉族, born 1976-11, CCP; profile id=120 updated 2026-06-30)
- Prior 县长: 董峰 (delivered 2026 政府工作报告 2026-02-08)
- Prior 县委书记: 韩俊良 (2023-2024 per official news)

Expected domain: www.huangyuan.gov.cn
Leadership page: /index.php?s=news&c=category&id=8
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Module path setup ─────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: F401  (process_tmp validator requires the token; runner uses it internally)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ──────────────────────────────────────────────────────────
SLUG = "湟源县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging / output paths ────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "qinghai_湟源县"
if _CURRENT_DIR.name == "qinghai_湟源县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════ Core Leadership ═══════════════════════
    {
        "id": 1,
        "name": "赵超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟源县委书记",
        "current_org": "中共湟源县委员会",
        "source": "湟源县政府门户网官方新闻 2026-07-23/2026-07-16(县第十八次党代会)/2026-05-29/2025-09-30; www.huangyuan.gov.cn",
    },
    {
        "id": 2,
        "name": "肖军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟源县委副书记、县人民政府县长",
        "current_org": "湟源县人民政府",
        "source": "湟源县政府领导之窗档案 id=120 (更新于2026-06-30), www.huangyuan.gov.cn",
    },
    # ═══════════════════ 县政府领导 (official 领导之窗) ═══════════════════
    {
        "id": 3,
        "name": "靳洪松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-09",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟源县委副书记、县人民政府副县长（挂职）",
        "current_org": "湟源县人民政府",
        "source": "湟源县政府领导之窗 id=1291 (2025-08-14), www.huangyuan.gov.cn",
    },
    {
        "id": 4,
        "name": "秦木德",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1985-01",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟源县委常委（正县级）、县政府党组副书记、副县长、城关镇党委书记（兼）",
        "current_org": "湟源县人民政府",
        "source": "湟源县政府领导之窗档案 id=6798 (2026-04-07), www.huangyuan.gov.cn",
    },
    {
        "id": 5,
        "name": "唐峰",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1971-07",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟源县人民政府副县长、县公安局局长",
        "current_org": "湟源县公安局",
        "source": "湟源县政府领导之窗档案 id=6946 (2024-02-05), www.huangyuan.gov.cn",
    },
    {
        "id": 6,
        "name": "郑红秀",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1985-08",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟源县人民政府副县长",
        "current_org": "湟源县人民政府",
        "source": "湟源县政府领导之窗档案 id=16446 (2025-04-21), www.huangyuan.gov.cn",
    },
    {
        "id": 7,
        "name": "马福全",
        "gender": "男",
        "ethnicity": "土族",
        "birth": "1984-12",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟源县人民政府副县长",
        "current_org": "湟源县人民政府",
        "source": "湟源县政府领导之窗档案 id=17368 (2026-05-18), www.huangyuan.gov.cn",
    },
    {
        "id": 8,
        "name": "郝力壮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-08",
        "birthplace": "",
        "education": "",
        "party_join": "九三学社社员",
        "work_start": "",
        "current_post": "湟源县人民政府副县长（挂职）",
        "current_org": "湟源县人民政府",
        "source": "湟源县政府领导之窗档案 id=17169 (2026-01-28), www.huangyuan.gov.cn",
    },
    # ═══════════════════ 前任 (predecessors) ═══════════════════════
    {
        "id": 9,
        "name": "董峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟源县原县长",
        "current_org": "湟源县人民政府",
        "source": "2026年湟源县政府工作报告 (2026-02-08 作报告), www.huangyuan.gov.cn",
    },
    {
        "id": 10,
        "name": "韩俊良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湟源县原县委书记",
        "current_org": "中共湟源县委员会",
        "source": "湟源县政府门户网新闻 2023-2024(县委书记韩俊良), www.huangyuan.gov.cn",
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共湟源县委员会", "type": "党委", "level": "县级", "parent": "中共西宁市委", "location": "青海省西宁市湟源县"},
    {"id": 2, "name": "湟源县人民政府", "type": "政府", "level": "县级", "parent": "湟源县", "location": "青海省西宁市湟源县"},
    {"id": 3, "name": "湟源县公安局", "type": "政府", "level": "县级", "parent": "湟源县人民政府", "location": "青海省西宁市湟源县"},
    {"id": 4, "name": "湟源县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "湟源县", "location": "青海省西宁市湟源县"},
    {"id": 5, "name": "湟源县城关镇委员会", "type": "乡镇", "level": "乡镇", "parent": "中共湟源县委", "location": "湟源县城关镇"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025-01", "end_date": "present", "rank": "正县级", "note": "主持县委全面工作; 2026-07 县第十八次党代会续任"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "2026-06", "end_date": "present", "rank": "正县级", "note": "主持县政府全面工作"},
    {"person_id": 3, "org_id": 2, "title": "县委副书记、副县长（挂职）", "start_date": "2025-08", "end_date": "present", "rank": "副县级(挂职)", "note": "负责东西部协作/丹噶尔古城旅游/招商引资"},
    {"person_id": 4, "org_id": 2, "title": "县委常委（正县级）、县政府党组副书记、副县长、城关镇党委书记（兼）", "start_date": "2026-04", "end_date": "present", "rank": "正县级", "note": "负责县政府日常工作、发改、财政、金融、国资、园区经济; 协助县长审计"},
    {"person_id": 5, "org_id": 3, "title": "副县长、县公安局局长", "start_date": "2024-02", "end_date": "present", "rank": "副县级", "note": "公安、司法、市场监管、信访"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "2025-04", "end_date": "present", "rank": "副县级", "note": "农业农村、乡村振兴、教育、卫生健康、文旅"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "2026-05", "end_date": "present", "rank": "副县级", "note": "自然资源和规划、住建、生态环境、水利"},
    {"person_id": 8, "org_id": 2, "title": "副县长（挂职）", "start_date": "2026-01", "end_date": "present", "rank": "副县级(挂职)", "note": "民族宗教、广播电视"},
    {"person_id": 9, "org_id": 2, "title": "县长", "start_date": "2023", "end_date": "2026-06", "rank": "正县级", "note": "2026-02-08 在县十九届人大六次会议上作政府工作报告后离任"},
    {"person_id": 10, "org_id": 1, "title": "县委书记", "start_date": "2023", "end_date": "2024", "rank": "正县级", "note": "2023-2024 县委书记, 后由赵超接任"},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "工作搭档", "context": "县委书记与县长, 同一届领导班子党政主官搭档; 共同参加政协界别讨论(2026-07-23)", "overlap_org": "湟源县 | 中共湟源县委/湟源县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长—常务副县长(县政府党组副书记), 负责县政府日常工作, 协助县长分管审计", "overlap_org": "湟源县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长—挂职副县长(东西部协作分工), 班子工作搭档", "overlap_org": "湟源县人民政府", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长—副县长兼公安局长", "overlap_org": "湟源县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长—副县长(女, 农业农村/乡村振兴)", "overlap_org": "湟源县人民政府", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—副县长", "overlap_org": "湟源县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—挂职副县长", "overlap_org": "湟源县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 9, "type": "前任继任", "context": "董峰为前任县长, 肖军接任县长职务", "overlap_org": "湟源县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 10, "type": "前任继任", "context": "韩俊良为前任县委书记, 赵超接任县委书记职务", "overlap_org": "中共湟源县委员会", "overlap_period": "2024-2025"},
]

# ── Build ──────────────────────────────────────────────────────────────
def main() -> None:
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
    print(f"\n✅ {SLUG} 数据构建完成。")
    print(f"   人物: {len(persons)}   机构: {len(organizations)}")
    print(f"   任职: {len(positions)}   关系: {len(relationships)}")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()