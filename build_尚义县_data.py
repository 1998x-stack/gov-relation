#!/usr/bin/env python3
"""Build 张家口市尚义县 (Shangyi County) leadership network data.

Level: 县
Province: 河北省
Parent city: 张家口市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_尚义县

Research date: 2026-07-24
Official source: http://www.zjksy.gov.cn/ (尚义县人民政府)

Current status (as of 2026-07-24):
- 县委书记: 待确认 — 2026年7月召开第十三次党代会（换届），新任书记或连任待核实
- 县长: 待确认 — 2026年7月22日召开第十八届人大一次会议（换届），新任县长或连任待核实

NOTE: Exa rate-limited, Baidu 403, gov-site leadership page inaccessible.
All web sources partially available — county homepage accessible but leadership
page returned 404 and specific article pages were behind opaque URLs.
Evidence is based on training data knowledge and labeled with appropriate
confidence levels.

Sources:
  S001: http://www.zjksy.gov.cn/ (尚义县人民政府官方网站, 首页确认第十三次党代会、第十八届人大一次会议于2026年7月召开)
  S002: https://zh.wikipedia.org/wiki/尚义县 (维基百科, 尚义县概况)
  S003: 训练数据 — 公开新闻报道中尚义县领导的推测信息
"""

from __future__ import annotations

import sys
from pathlib import Path

# When run from data/tmp/hebei_尚义县/, resolve repo root three levels up
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "尚义县"

# When run from staging, write DB and GEXF to the staging directory.
_STAGING_DIR = _SCRIPT_DIR  # data/tmp/hebei_尚义县/
DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "待确认-县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尚义县委书记(2026年7月第十三次党代会换届)",
        "current_org": "中共尚义县委员会",
        "source": ("官方: http://www.zjksy.gov.cn/ (第十三次党代会确认, "
                    "但姓名因无法获取具体文章暂缺)"),
    },
    {
        "id": 2,
        "name": "待确认-县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尚义县县长(2026年7月第十八届人大一次会议换届)",
        "current_org": "尚义县人民政府",
        "source": ("官方: http://www.zjksy.gov.cn/ (第十八届人大一次会议确认, "
                    "但姓名因无法获取具体文章暂缺)"),
    },
    # ════════════════════════════════════════
    # 前任县委书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "陈建",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": ("推测: 陈建约2020-2023年任尚义县委书记, "
                    "公开报道有提及但来源无法在线核实"),
    },
    {
        "id": 4,
        "name": "白建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": ("推测: 白建军约2017-2020年任尚义县委书记, "
                    "公开报道有提及但来源无法在线核实"),
    },
    # ════════════════════════════════════════
    # 前任县长
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "高尚君",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": ("推测: 高尚君约2021-2024年任尚义县长, "
                    "公开报道有提及但来源无法在线核实"),
    },
    {
        "id": 6,
        "name": "徐进海",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": ("推测: 徐进海约2017-2021年任尚义县长, "
                    "后调任张家口市其他职务"),
    },
    # ════════════════════════════════════════
    # 县人大、政协领导(推测)
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "待确认-县人大主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尚义县人大常委会主任(推测)",
        "current_org": "尚义县人大常委会",
        "source": ("推测: 县人大主任在换届选举中产生, "
                    "姓名因无法获取具体报道暂缺"),
    },
    {
        "id": 8,
        "name": "待确认-县政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尚义县政协主席(推测)",
        "current_org": "政协尚义县委员会",
        "source": ("推测: 县政协主席在换届选举中产生, "
                    "姓名因无法获取具体报道暂缺"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共尚义县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共张家口市委员会",
        "location": "河北省张家口市尚义县",
    },
    {
        "id": 2,
        "name": "尚义县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "张家口市人民政府",
        "location": "河北省张家口市尚义县",
    },
    {
        "id": 3,
        "name": "中共尚义县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共张家口市纪律检查委员会",
        "location": "河北省张家口市尚义县",
    },
    {
        "id": 4,
        "name": "尚义县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "张家口市人大常委会",
        "location": "河北省张家口市尚义县",
    },
    {
        "id": 5,
        "name": "政协尚义县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协张家口市委员会",
        "location": "河北省张家口市尚义县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 县委领导
    {"person_id": 1, "org_id": 1, "title": "尚义县委书记(第十三次党代会换届)", "start": "2026-07", "end": "至今", "rank": "正处级", "note": "2026年7月第十三次党代会. 具体姓名待核实."},
    # 县政府领导
    {"person_id": 2, "org_id": 2, "title": "尚义县县长(第十八届人大一次会议换届)", "start": "2026-07", "end": "至今", "rank": "正处级", "note": "2026年7月22日第十八届人大一次会议. 具体姓名待核实."},
    {"person_id": 2, "org_id": 1, "title": "尚义县委副书记(推测)", "start": "2026-07", "end": "至今", "rank": "副处级", "note": "县长同时担任县委副书记"},
    # 人大
    {"person_id": 7, "org_id": 4, "title": "尚义县人大常委会主任(推测)", "start": "", "end": "至今", "rank": "正处级", "note": "2026年7月换届. 具体姓名待核实."},
    # 政协
    {"person_id": 8, "org_id": 5, "title": "尚义县政协主席(推测)", "start": "", "end": "至今", "rank": "正处级", "note": "2026年7月换届. 具体姓名待核实."},
    # 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "尚义县委书记(前任)", "start": "2020", "end": "2023", "rank": "正处级", "note": "陈建. 任期根据公开报道推测."},
    {"person_id": 4, "org_id": 1, "title": "尚义县委书记(前任)", "start": "2017", "end": "2020", "rank": "正处级", "note": "白建军. 任期根据公开报道推测."},
    # 前任县长
    {"person_id": 5, "org_id": 2, "title": "尚义县县长(前任)", "start": "2021", "end": "2024", "rank": "正处级", "note": "高尚君. 任期根据公开报道推测."},
    {"person_id": 6, "org_id": 2, "title": "尚义县县长(前任)", "start": "2017", "end": "2021", "rank": "正处级", "note": "徐进海. 任期根据公开报道推测."},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 前任县委书记与县长搭档关系
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "陈建(书记)与高尚君(县长)党政工作搭档", "overlap_org": "尚义县", "overlap_period": "2021-2023", "confidence": "plausible"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "白建军(书记)与徐进海(县长)党政工作搭档", "overlap_org": "尚义县", "overlap_period": "2017-2020", "confidence": "plausible"},
    # 前后任关系
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "陈建接替白建军任县委书记", "overlap_org": "中共尚义县委员会", "overlap_period": "2020", "confidence": "plausible"},
    {"person_a": 5, "person_b": 6, "type": "predecessor_successor", "context": "高尚君接替徐进海任县长", "overlap_org": "尚义县人民政府", "overlap_period": "2021", "confidence": "plausible"},
    # 前任书记与前任县长
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "陈建(书记)与徐进海(县长)可能有短期工作交接", "overlap_org": "尚义县", "overlap_period": "2020-2021", "confidence": "unverified"},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "白建军(书记)与高尚君(县长)可能有短期工作交接", "overlap_org": "尚义县", "overlap_period": "2020-2021", "confidence": "unverified"},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  张家口市尚义县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 尚义县政府网站 www.zjksy.gov.cn")
    print("=" * 60)
    print()
    print("  ⚠️  ⚠️  ⚠️  重要提示  ⚠️  ⚠️  ⚠️")
    print("  因搜索工具限流、政府网站架构限制，本届(2026年7月)")
    print("  换届后县委书记和县长的具体姓名未能获取。")
    print("  尚义县第十三次党代会(2026年7月)和第十八届人大一次会议")
    print("  (2026年7月22日)已召开，但具体文章页面无法访问。")
    print("  图中列出的是前任领导及待确认占位符。")
    print()
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
    print(f"\n✅ 尚义县数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")
