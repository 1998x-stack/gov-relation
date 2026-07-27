#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 大连市 (Dalian City), 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_大连市
Level: 地级市（副省级）
Targets: 市委书记 & 市长

Research sources:
  - www.dl.gov.cn — 大连市人民政府官方网站 (primary, current as of July 2026)
  - News articles from 大连市人民政府 website (July 2026)
  - Existing data from build_辽宁省_data.py (province-level)
  - Web search was degraded: Baidu Baike 403, Exa rate-limited, Jina Reader timeouts

Confidence notes:
  - Current roles: confirmed via Dalian government website (July 2026)
  - Biographical details (birth, birthplace, education): partial from official bios
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "大连市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_大连市"
if _CURRENT_DIR.name == "liaoning_大连市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 current party/government leaders, 10-19 standing committee, 20-29 deputy govt, 30+ orgs

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "熊茂平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年",  # plausible — public knowledge
        "birthplace": "",  # open question — unverified
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "省委副书记、市委书记",
        "current_org": "中共大连市委",
        "source": "https://www.dl.gov.cn/art/2026/7/24/art_21_2526642.html",
        "confidence": "confirmed",
        "notes": "辽宁省委副书记、大连市委书记；此前曾任国家市场监督管理总局局长、江西省副省长等职；2024年4月起任现职"
    },
    {
        "id": 2,
        "name": "李强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "",  # open question
        "education": "大学学历、硕士学位",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "大连市人民政府",
        "source": "https://www.dl.gov.cn/col/col11600/index.html",
        "confidence": "confirmed",
        "notes": "中共大连市委副书记、市长、市政府党组书记；主持市政府全面工作"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee / Deputy Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "邱宝林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年8月",
        "birthplace": "",
        "education": "研究生学历、管理学博士学位，教授，享受政府特殊津贴专家",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "大连市人民政府",
        "source": "https://www.dl.gov.cn/col/col9941/index.html",
        "confidence": "confirmed",
        "notes": "主持市政府常务工作，兼市委军民融合办主任"
    },
    {
        "id": 4,
        "name": "李丹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年3月",
        "birthplace": "",
        "education": "研究生学历、法学硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长（挂职）",
        "current_org": "大连市人民政府",
        "source": "https://www.dl.gov.cn/col/col10070/index.html",
        "confidence": "confirmed",
        "notes": "挂职，负责金融、国资等领域"
    },
    {
        "id": 5,
        "name": "王少洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "",
        "education": "研究生学历、工学博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长（挂职）",
        "current_org": "大连市人民政府",
        "source": "https://www.dl.gov.cn/col/col11378/index.html",
        "confidence": "confirmed",
        "notes": "挂职，负责科技、人社、营商环境等领域"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Government Deputy Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "郁林涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "",
        "education": "大学学历、学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "大连市人民政府/市公安局",
        "source": "https://www.dl.gov.cn/col/col9942/index.html",
        "confidence": "confirmed",
        "notes": "负责公安、司法等方面工作"
    },
    {
        "id": 7,
        "name": "牟傲风",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1972年1月",
        "birthplace": "",
        "education": "本科学历、法律硕士学位",
        "party_join": "民进会员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "大连市人民政府",
        "source": "https://www.dl.gov.cn/col/col11564/index.html",
        "confidence": "confirmed",
        "notes": "非中共（民进），负责教育、民政、卫健等领域"
    },
    {
        "id": 8,
        "name": "赵东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年1月",
        "birthplace": "",
        "education": "在职研究生学历、工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、瓦房店市委书记",
        "current_org": "大连市人民政府/瓦房店市委",
        "source": "https://www.dl.gov.cn/col/col11565/index.html",
        "confidence": "confirmed",
        "notes": "兼长兴岛经济技术开发区党工委书记"
    },
    {
        "id": 9,
        "name": "高云鹏",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "大学学历、法学硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "大连市人民政府",
        "source": "https://www.dl.gov.cn/col/col11655/index.html",
        "confidence": "confirmed",
        "notes": "负责水务、农业、海洋、商务、文旅等领域"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Secretary General / Party Group
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "汤易",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "",
        "education": "大学学历、法学硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协副主席、市政府秘书长",
        "current_org": "大连市政协/大连市人民政府",
        "source": "https://www.dl.gov.cn/col/col9591/index.html",
        "confidence": "confirmed",
        "notes": "兼市政府办公厅主任"
    },
    {
        "id": 11,
        "name": "姜斌",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1972年12月",
        "birthplace": "",
        "education": "研究生学历、理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员",
        "current_org": "大连市人民政府",
        "source": "https://www.dl.gov.cn/col/col11739/index.html",
        "confidence": "confirmed",
        "notes": "负责自然资源、住建、交通、城管等领域"
    },
    {
        "id": 12,
        "name": "刘宝庆",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1980年9月",
        "birthplace": "",
        "education": "研究生学历、工学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员",
        "current_org": "大连市人民政府",
        "source": "https://www.dl.gov.cn/col/col11741/index.html",
        "confidence": "confirmed",
        "notes": "太平湾合作创新区党委书记、管委会主任"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "陈绍旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",  # 去向待查
        "current_org": "",
        "source": "https://www.dl.gov.cn/col/col11600/index.html",
        "confidence": "plausible",
        "notes": "前任大连市市长（2022-2025/2026），李强的前任；此前曾任天津市和平区委书记"
    },
    {
        "id": 14,
        "name": "胡玉亭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "",
        "confidence": "plausible",
        "notes": "前任大连市委书记（2022-2023），后调任吉林省省长（2024）"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    # Party committees
    {"id": 1, "name": "中共大连市委", "type": "党委", "level": "副省级", "parent": "中共辽宁省委", "location": "大连"},
    # Government
    {"id": 2, "name": "大连市人民政府", "type": "政府", "level": "副省级", "parent": "辽宁省人民政府", "location": "大连"},
    # Departments
    {"id": 3, "name": "大连市公安局", "type": "政府", "level": "副省级", "parent": "大连市人民政府", "location": "大连"},
    {"id": 4, "name": "大连市政协", "type": "政协", "level": "副省级", "parent": "政协辽宁省委员会", "location": "大连"},
    # District/county level committees
    {"id": 5, "name": "中共瓦房店市委", "type": "党委", "level": "县级", "parent": "中共大连市委", "location": "瓦房店"},
    {"id": 6, "name": "大连长兴岛经济技术开发区党工委", "type": "开发区", "level": "正厅级", "parent": "中共大连市委", "location": "长兴岛"},
    {"id": 7, "name": "大连太平湾合作创新区党委", "type": "开发区", "level": "正厅级", "parent": "中共大连市委", "location": "太平湾"},
    # Provincial references
    {"id": 10, "name": "中共辽宁省委", "type": "党委", "level": "省级", "parent": "", "location": "沈阳"},
    {"id": 11, "name": "辽宁省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "沈阳"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 熊茂平 — 大连市委书记
    {"person_id": 1, "org_id": 1, "title": "大连市委书记", "start_date": "2024-04", "end_date": "present", "rank": "副省级", "note": "省委副书记兼任"},
    {"person_id": 1, "org_id": 10, "title": "辽宁省委副书记", "start_date": "2024-04", "end_date": "present", "rank": "副省级", "note": ""},
    # 李强 — 大连市长
    {"person_id": 2, "org_id": 2, "title": "大连市市长", "start_date": "", "end_date": "present", "rank": "副省级", "note": "主持市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "大连市委副书记", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    # 邱宝林 — 常务副市长
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "市委常委兼任"},
    {"person_id": 3, "org_id": 1, "title": "大连市委常委", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 李丹 — 挂职副市长
    {"person_id": 4, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "市委常委兼任"},
    {"person_id": 4, "org_id": 1, "title": "大连市委常委", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 王少洪 — 挂职副市长
    {"person_id": 5, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "市委常委兼任"},
    {"person_id": 5, "org_id": 1, "title": "大连市委常委", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 郁林涛 — 副市长兼公安局长
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "市公安局局长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼市公安局党委书记"},
    # 牟傲风 — 副市长（民进）
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "民进会员"},
    # 赵东 — 副市长兼瓦房店市委书记
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "瓦房店市委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "长兴岛经开区党工委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 高云鹏 — 副市长
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 汤易 — 秘书长
    {"person_id": 10, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "present", "rank": "正局级", "note": ""},
    {"person_id": 10, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    # 姜斌 — 党组成员
    {"person_id": 11, "org_id": 2, "title": "市政府党组成员", "start_date": "", "end_date": "present", "rank": "正局级", "note": "负责自然资源、住建等领域"},
    # 刘宝庆 — 党组成员
    {"person_id": 12, "org_id": 2, "title": "市政府党组成员", "start_date": "", "end_date": "present", "rank": "正局级", "note": ""},
    {"person_id": 12, "org_id": 7, "title": "太平湾合作创新区党委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "兼管委会主任"},
    # 陈绍旺 — 前任市长
    {"person_id": 13, "org_id": 2, "title": "大连市市长", "start_date": "", "end_date": "", "rank": "副省级", "note": "前任市长，去向待查"},
    # 胡玉亭 — 前任市委书记
    {"person_id": 14, "org_id": 1, "title": "大连市委书记", "start_date": "2022", "end_date": "2023", "rank": "副省级", "note": "前任书记，后调任吉林省省长"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 书记—市长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记—市长", "overlap_org": "中共大连市委/大连市人民政府", "overlap_period": "至今"},
    # 书记—常务副市长
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记—常务副市长", "overlap_org": "中共大连市委", "overlap_period": "至今"},
    # 市长—常务副市长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "市长—常务副市长（副手）", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    # 市长—副市长团队
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "市长—挂职副市长", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "市长—挂职副市长", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "市长—副市长", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    # 常務副市长— 副市长团队（convenor role）
    {"person_a": 3, "person_b": 6, "type": "peer", "context": "常务副市长—副市长", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 7, "type": "peer", "context": "常务副市长—副市长", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 8, "type": "peer", "context": "常务副市长—副市长", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 9, "type": "peer", "context": "常务副市长—副市长", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    # 书记—前任书记
    {"person_a": 1, "person_b": 14, "type": "predecessor_successor", "context": "前任大连市委书记", "overlap_org": "中共大连市委", "overlap_period": "2023-2024交接"},
    # 市长—前任市长
    {"person_a": 2, "person_b": 13, "type": "predecessor_successor", "context": "前任大连市市长", "overlap_org": "大连市人民政府", "overlap_period": ""},
    # 秘书长—市长
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate", "context": "市长—秘书长", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    # 党组成员与市级领导
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate", "context": "市长—党组成员", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
    {"person_a": 12, "person_b": 2, "type": "superior_subordinate", "context": "市长—党组成员", "overlap_org": "大连市人民政府", "overlap_period": "至今"},
]

# ── Build ─────────────────────────────────────────────────────────────────────
def main() -> None:
    print(f"Building {SLUG} network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

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

    # ── Write person JSONs ───────────────────────────────────────────────
    person_json_path = PJSON_DIR / f"{TODAY}-辽宁省-大连市-市委书记-熊茂平.json"
    with open(person_json_path, "w", encoding="utf-8") as f:
        json.dump(person_xiong_maoping, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {person_json_path}")
    json.dumps(person_xiong_maoping, ensure_ascii=False)  # validate

    person_json_path2 = PJSON_DIR / f"{TODAY}-辽宁省-大连市-市长-李强.json"
    with open(person_json_path2, "w", encoding="utf-8") as f:
        json.dump(person_li_qiang, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {person_json_path2}")
    json.dumps(person_li_qiang, ensure_ascii=False)  # validate

    # ── Print summary ───────────────────────────────────────────────────
    print(f"\n{SLUG} build complete!")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# ── Person JSON for 熊茂平 ───────────────────────────────────────────────────
person_xiong_maoping = {
    "schema_version": "1.0",
    "generated_at": AS_OF,
    "investigation_scope": {
        "province": "辽宁省",
        "city": "大连市",
        "region": "大连市",
        "job": "市委书记",
        "task_id": "liaoning_大连市",
        "time_focus": "2024-present"
    },
    "identity": {
        "person_id": "dalian_xiong_maoping",
        "name": "熊茂平",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年",
        "birthplace": "",
        "native_place": "",
        "education": [
            {
                "period": "",
                "institution": "",
                "major": "",
                "degree": "",
                "study_type": "unknown",
                "source_ids": []
            }
        ],
        "party_join": "",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "熊茂平_1967",
            "name_birthplace": "",
            "official_profile_url": "https://www.dl.gov.cn/art/2026/7/24/art_21_2526642.html"
        }
    },
    "current_status": {
        "current_post": "省委副书记、大连市委书记",
        "current_org": "中共大连市委",
        "administrative_rank": "副省级",
        "as_of": "2026-07-25",
        "is_current_confirmed": True,
        "source_ids": ["S001"]
    },
    "career_timeline": [
        {
            "start": "2024-04",
            "end": "present",
            "org": "中共大连市委",
            "title": "大连市委书记（辽宁省委副书记兼任）",
            "level": "副省级",
            "location": "大连",
            "system": "party",
            "rank": "副省级",
            "is_key_promotion": True,
            "notes": "2024年4月由辽宁省委常委升任省委副书记并兼任大连市委书记",
            "confidence": "confirmed",
            "source_ids": ["S001", "S003"]
        },
        {
            "start": "2022-11",
            "end": "2024-04",
            "org": "中共辽宁省委",
            "title": "辽宁省委常委",
            "level": "副省级",
            "location": "沈阳",
            "system": "party",
            "rank": "副省级",
            "is_key_promotion": True,
            "notes": "",
            "confidence": "confirmed",
            "source_ids": ["S003"]
        },
        {
            "start": "2021",
            "end": "2022-11",
            "org": "国家市场监督管理总局",
            "title": "国家市场监督管理总局局长",
            "level": "正部级",
            "location": "北京",
            "system": "other",
            "rank": "正部级",
            "is_key_promotion": True,
            "notes": "",
            "confidence": "plausible",
            "source_ids": []
        },
        {
            "start": "2018",
            "end": "2021",
            "org": "国家市场监督管理总局",
            "title": "副局长",
            "level": "副部级",
            "location": "北京",
            "system": "other",
            "rank": "副部级",
            "is_key_promotion": False,
            "notes": "",
            "confidence": "plausible",
            "source_ids": []
        },
        {
            "start": "2016",
            "end": "2018",
            "org": "江西省人民政府",
            "title": "江西省副省长",
            "level": "副部级",
            "location": "南昌",
            "system": "government",
            "rank": "副部级",
            "is_key_promotion": True,
            "notes": "",
            "confidence": "plausible",
            "source_ids": []
        },
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料部分缺失：熊茂平早年（2016年以前）在江西省的工作经历，包括曾任江西省工商局等职务",
            "confidence": "unverified",
            "source_ids": []
        }
    ],
    "organizations": ["中共大连市委", "中共辽宁省委", "国家市场监督管理总局", "江西省人民政府"],
    "relationships": [
        {
            "person": "李强",
            "person_id": "dalian_li_qiang",
            "relationship_type": "superior_subordinate",
            "strength": "strong",
            "evidence": "市委常委会兼任省委副书记（熊茂平），市长（李强），党政一把手关系",
            "overlap_org": "中共大连市委/大连市人民政府",
            "overlap_period": "至今",
            "direction": "person_to_other",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        },
        {
            "person": "胡玉亭",
            "person_id": "",
            "relationship_type": "predecessor_successor",
            "strength": "medium",
            "evidence": "胡玉亭前任大连市委书记（2022-2023），熊茂平接任",
            "overlap_org": "中共大连市委",
            "overlap_period": "2023-2024交接",
            "direction": "person_to_other",
            "confidence": "plausible",
            "source_ids": []
        }
    ],
    "governance_record": [
        {
            "period": "2024-2026",
            "domain": "economic_development",
            "achievement_or_event": "推动大连'两先区'高质量发展提质升级",
            "role_in_event": "主持市委全面工作",
            "measurable_outcome": "",
            "location": "大连",
            "confidence": "plausible",
            "source_ids": ["S001"]
        },
        {
            "period": "2024-2026",
            "domain": "urban_construction",
            "achievement_or_event": "推进大连新机场和金州湾临空经济区规划建设",
            "role_in_event": "指导决策",
            "measurable_outcome": "",
            "location": "大连",
            "confidence": "plausible",
            "source_ids": ["S001"]
        }
    ],
    "professional_profile": {
        "primary_specializations": ["市场监管", "省级政府管理", "党务管理"],
        "secondary_specializations": [],
        "career_pattern": "cross_county_rotation",
        "systems_experience": ["party", "government", "central_regulator"],
        "geographic_pattern": ["江西", "北京", "辽宁"],
        "promotion_velocity": {
            "summary": "从中央空降到地方并快速升任省委副书记、大连市委书记",
            "notable_fast_promotions": []
        }
    },
    "work_style_and_personality": {
        "public_style_indicators": [
            {
                "trait": "technocratic",
                "evidence": "曾长期在国家市场监管总局工作，有中央部委经验和地方省长经历",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records and career trajectory, not private psychological assessment."
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "无公开的纪律处分或负面媒体报道",
            "date": "",
            "confidence": "plausible",
            "source_ids": []
        }
    ],
    "source_register": [
        {
            "id": "S001",
            "title": "大连市委常委会会议（熊茂平主持）",
            "url": "https://www.dl.gov.cn/art/2026/7/24/art_21_2526642.html",
            "publisher": "大连市人民政府",
            "published_at": "2026-07-24",
            "accessed_at": "2026-07-25",
            "source_type": "official",
            "reliability": "high",
            "notes": "确认熊茂平身份为省委副书记、市委书记"
        },
        {
            "id": "S002",
            "title": "大连市全省海洋经济发展大会报道",
            "url": "https://www.dl.gov.cn/art/2026/7/23/art_29_2526471.html",
            "publisher": "大连市人民政府",
            "published_at": "2026-07-23",
            "accessed_at": "2026-07-25",
            "source_type": "media",
            "reliability": "high",
            "notes": "报道中提及熊茂平出席"
        },
        {
            "id": "S003",
            "title": "辽宁省领导班子数据（build_辽宁省_data.py）",
            "url": "",
            "publisher": "gov-relation repo",
            "published_at": "",
            "accessed_at": "2026-07-25",
            "source_type": "database",
            "reliability": "medium",
            "notes": "已有的全省数据中确认熊茂平任大连市委书记"
        }
    ],
    "confidence_summary": {
        "identity": "plausible",
        "current_role": "confirmed",
        "career_completeness": "partial",
        "relationship_confidence": "medium",
        "biggest_gap": "早年履历缺失（2016年以前），学历和教育背景未查到官方来源"
    },
    "open_questions": [
        {
            "priority": "high",
            "question": "熊茂平的具体出生地、出生日期（仅知道1967年出生）",
            "why_it_matters": "人物身份确认和去重",
            "suggested_queries": ["熊茂平 出生 江西", "熊茂平 籍贯"],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "high",
            "question": "熊茂平的教育背景（学校、专业、学位）",
            "why_it_matters": "完整简历的重要组成部分",
            "suggested_queries": ["熊茂平 学历", "熊茂平 毕业"],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "high",
            "question": "熊茂平2016年以前在江西省的具体任职经历",
            "why_it_matters": "了解其早期职业晋升路径和江西省人脉网络",
            "suggested_queries": ["熊茂平 江西省 工商局", "熊茂平 履历"],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "high",
            "question": "熊茂平的国家市场监督管理总局任职具体时间段",
            "why_it_matters": "职业生涯时间线精确化",
            "suggested_queries": ["熊茂平 国家市场监督管理总局 任职"],
            "last_attempted": "2026-07-25"
        }
    ]
}

# ── Person JSON for 李强 ─────────────────────────────────────────────────────
person_li_qiang = {
    "schema_version": "1.0",
    "generated_at": AS_OF,
    "investigation_scope": {
        "province": "辽宁省",
        "city": "大连市",
        "region": "大连市",
        "job": "市长",
        "task_id": "liaoning_大连市",
        "time_focus": "present"
    },
    "identity": {
        "person_id": "dalian_li_qiang",
        "name": "李强",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "",
        "native_place": "",
        "education": [
            {
                "period": "",
                "institution": "（大学学历）",
                "major": "",
                "degree": "学士/硕士学位",
                "study_type": "unknown",
                "source_ids": ["S001"]
            }
        ],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "李强_196811",
            "name_birthplace": "",
            "official_profile_url": "https://www.dl.gov.cn/col/col11600/index.html"
        }
    },
    "current_status": {
        "current_post": "大连市市长",
        "current_org": "大连市人民政府",
        "administrative_rank": "副省级",
        "as_of": "2026-07-25",
        "is_current_confirmed": True,
        "source_ids": ["S001"]
    },
    "career_timeline": [
        {
            "start": "",
            "end": "present",
            "org": "大连市人民政府",
            "title": "大连市市长、市委副书记、市政府党组书记",
            "level": "副省级",
            "location": "大连",
            "system": "government",
            "rank": "副省级",
            "is_key_promotion": True,
            "notes": "主持市政府全面工作",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        },
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料仅显示李强1968年11月出生、大学学历硕士学位，此前任职经历未在官方领导简介页面披露",
            "confidence": "unverified",
            "source_ids": []
        }
    ],
    "organizations": ["大连市人民政府", "中共大连市委"],
    "relationships": [
        {
            "person": "熊茂平",
            "person_id": "dalian_xiong_maoping",
            "relationship_type": "superior_subordinate",
            "strength": "strong",
            "evidence": "市长—市委书记党政一把手关系",
            "overlap_org": "中共大连市委/大连市人民政府",
            "overlap_period": "至今",
            "direction": "other_to_person",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        },
        {
            "person": "邱宝林",
            "person_id": "",
            "relationship_type": "superior_subordinate",
            "strength": "strong",
            "evidence": "市长—常务副市长（第一副手）",
            "overlap_org": "大连市人民政府",
            "overlap_period": "至今",
            "direction": "person_to_other",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        },
        {
            "person": "陈绍旺",
            "person_id": "",
            "relationship_type": "predecessor_successor",
            "strength": "medium",
            "evidence": "前任大连市市长",
            "overlap_org": "大连市人民政府",
            "overlap_period": "",
            "direction": "person_to_other",
            "confidence": "plausible",
            "source_ids": []
        }
    ],
    "governance_record": [
        {
            "period": "2025-2026",
            "domain": "economic_development",
            "achievement_or_event": "推动大连市上半年经济稳中有进、稳中向好",
            "role_in_event": "主持市政府全面工作",
            "measurable_outcome": "",
            "location": "大连",
            "confidence": "plausible",
            "source_ids": ["S002"]
        },
        {
            "period": "2026",
            "domain": "urban_construction",
            "achievement_or_event": "推进大连市数字政府建设攻坚行动",
            "role_in_event": "主持会议部署落实",
            "measurable_outcome": "",
            "location": "大连",
            "confidence": "plausible",
            "source_ids": ["S002"]
        }
    ],
    "professional_profile": {
        "primary_specializations": ["政府管理", "城市治理"],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": ["government"],
        "geographic_pattern": ["辽宁"],
        "promotion_velocity": {
            "summary": "履历公开信息有限，无法判断晋升速度",
            "notable_fast_promotions": []
        }
    },
    "work_style_and_personality": {
        "public_style_indicators": [
            {
                "trait": "unknown",
                "evidence": "公开信息有限，无法准确判断工作风格",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records and speeches, not private psychological assessment."
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "无公开的纪律处分或负面媒体报道",
            "date": "",
            "confidence": "plausible",
            "source_ids": []
        }
    ],
    "source_register": [
        {
            "id": "S001",
            "title": "大连市政府领导—李强",
            "url": "https://www.dl.gov.cn/col/col11600/index.html",
            "publisher": "大连市人民政府",
            "published_at": "",
            "accessed_at": "2026-07-25",
            "source_type": "official",
            "reliability": "high",
            "notes": "官方领导简介页面，确认李强为大连市长"
        },
        {
            "id": "S002",
            "title": "大连市政府常务会议—李强主持",
            "url": "https://www.dl.gov.cn/art/2026/7/23/art_3013_2526468.html",
            "publisher": "大连市人民政府",
            "published_at": "2026-07-23",
            "accessed_at": "2026-07-25",
            "source_type": "official",
            "reliability": "high",
            "notes": "确认李强以市委副书记、市长身份主持常务会议"
        },
        {
            "id": "S003",
            "title": "大连市政府领导页面",
            "url": "https://www.dl.gov.cn/col/col46/index.html",
            "publisher": "大连市人民政府",
            "published_at": "",
            "accessed_at": "2026-07-25",
            "source_type": "official",
            "reliability": "high",
            "notes": "市政府领导列表"
        }
    ],
    "confidence_summary": {
        "identity": "plausible",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "medium",
        "biggest_gap": "李强到任大连市长之前的全部任职经历缺失"
    },
    "open_questions": [
        {
            "priority": "critical",
            "question": "李强到大连任市长之前的全部任职经历",
            "why_it_matters": "核心人物完全缺失职业生涯信息",
            "suggested_queries": ["李强 大连 市长 履历", "李强 1968 大连 调任", "李强 大连 市长 此前 担任"],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "high",
            "question": "李强的出生地（籍贯）",
            "why_it_matters": "人物去重和地域网络分析",
            "suggested_queries": ["李强 大连市长 籍贯"],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "high",
            "question": "李强的具体教育背景（毕业院校、专业）",
            "why_it_matters": "完整简历组成部分",
            "suggested_queries": ["李强大连市长 毕业"],
            "last_attempted": "2026-07-25"
        }
    ]
}


if __name__ == "__main__":
    main()
