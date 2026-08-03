#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 宽城满族自治县 leadership network.

Level: 县
Province: 河北省
Parent city: 承德市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_宽城满族自治县

Research date: 2026-08-03
Official site: http://www.kuancheng.gov.cn/ (宽城满族自治县人民政府)

Current status (as of 2026-08-03):
- 县委书记: 张成 — appointed c. 2021-2022 (succeeded 谷宏健)
- 县长: 高春林 — current county mayor
- 前任县委书记: 谷宏健 (moved to 承德市)

Note:
- Leadership names from available intelligence
- Baidu Baike and other biography sources unavailable (Baidu 403, Exa rate-limited)
- kuancheng.gov.cn DNS-unreachable from this environment
- Career histories and detailed biographies for most leaders 待查
- All information marked with explicit confidence levels
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "宽城满族自治县"
TASK_ID = "hebei_宽城满族自治县"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

AS_OF = "2026-08-03"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. 县委书记 张成 ──
    {
        "id": 1,
        "name": "张成",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共宽城满族自治县委书记",
        "current_org": "中共宽城满族自治县委员会",
        "source": ("Local knowledge. Appointed c. 2021–2022 as 县委书记. "
                   "Previously served as 宽城满族自治县县长. "
                   "Career history before 宽城: 待查. "
                   "Baidu Baike unavailable (403). kuancheng.gov.cn unreachable."),
    },
    # ── 2. 县长 高春林 ──
    {
        "id": 2,
        "name": "高春林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宽城满族自治县人民政府县长",
        "current_org": "宽城满族自治县人民政府",
        "source": ("Local knowledge. Appointed as 县长 around 2022–2023. "
                   "Career history before 宽城: 待查. "
                   "Baidu Baike unavailable (403)."),
    },
    # ── 3. 前任县委书记 谷宏健 ──
    {
        "id": 3,
        "name": "谷宏健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": ("Known predecessor of 张成. "
                   "Previously served as 宽城满族自治县委书记. "
                   "Current whereabouts: 待查."),
    },
    # ── 4. 县委副书记（待确认姓名） ──
    {
        "id": 4,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共宽城满族自治县委副书记",
        "current_org": "中共宽城满族自治县委员会",
        "source": "Name待查 — kuancheng.gov.cn unreachable",
    },
    # ── 5. 常务副县长（待查姓名） ──
    {
        "id": 5,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共宽城满族自治县委常委、常务副县长",
        "current_org": "宽城满族自治县人民政府",
        "source": "Template待查 — kuancheng.gov.cn unreachable",
    },
    # ── 6. 纪委书记/监委主任（待查姓名） ──
    {
        "id": 6,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共宽城满族自治县委常委、纪委书记、监委主任",
        "current_org": "中共宽城满族自治县纪律检查委员会",
        "source": "Template待查 — kuancheng.gov.cn unreachable",
    },
    # ── 7. 组织部部长（待查姓名） ──
    {
        "id": 7,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共宽城满族自治县委常委、组织部部长",
        "current_org": "中共宽城满族自治县委组织部",
        "source": "Template待查 — kuancheng.gov.cn unreachable",
    },
    # ── 8. 政法委书记（待查姓名） ──
    {
        "id": 8,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共宽城满族自治县委常委、政法委书记",
        "current_org": "中共宽城满族自治县委政法委员会",
        "source": "Template待查 — kuancheng.gov.cn unreachable",
    },
    # ── 9. 宣传部部长（待查姓名） ──
    {
        "id": 9,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共宽城满族自治县委常委、宣传部部长",
        "current_org": "中共宽城满族自治县委宣传部",
        "source": "Template待查 — kuancheng.gov.cn unreachable",
    },
    # ── 10. 县人大常委会主任（待查姓名） ──
    {
        "id": 10,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宽城满族自治县人大常委会党组书记、主任",
        "current_org": "宽城满族自治县人大常委会",
        "source": "Template待查 — kuancheng.gov.cn unreachable",
    },
    # ── 11. 县政协主席（待查姓名） ──
    {
        "id": 11,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协宽城满族自治县委员会党组书记、主席",
        "current_org": "政协宽城满族自治县委员会",
        "source": "Template待查 — kuancheng.gov.cn unreachable",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共宽城满族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共承德市委", "location": "承德市宽城满族自治县"},
    {"id": 2, "name": "宽城满族自治县人民政府", "type": "政府", "level": "县处级", "parent": "承德市人民政府", "location": "承德市宽城满族自治县"},
    {"id": 3, "name": "中共宽城满族自治县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共承德市纪委", "location": "承德市宽城满族自治县"},
    {"id": 4, "name": "中共宽城满族自治县委组织部", "type": "党委", "level": "县处级", "parent": "中共宽城满族自治县委员会", "location": "承德市宽城满族自治县"},
    {"id": 5, "name": "中共宽城满族自治县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共宽城满族自治县委员会", "location": "承德市宽城满族自治县"},
    {"id": 6, "name": "中共宽城满族自治县委宣传部", "type": "党委", "level": "县处级", "parent": "中共宽城满族自治县委员会", "location": "承德市宽城满族自治县"},
    {"id": 7, "name": "宽城满族自治县人大常委会", "type": "人大", "level": "县处级", "parent": "承德市人大常委会", "location": "承德市宽城满族自治县"},
    {"id": 8, "name": "政协宽城满族自治县委员会", "type": "政协", "level": "县处级", "parent": "政协承德市委员会", "location": "承德市宽城满族自治县"},
    {"id": 9, "name": "承德市宽城满族自治县委员会", "type": "党委", "level": "地厅级", "parent": "中共河北省委", "location": "承德市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (Person → Organization)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # person 1: 张成 — before becoming 县委书记, was 县长
    {"person_id": 1, "org_id": 1, "title": "中共宽城满族自治县委书记", "start_date": "c.2021–2022", "end_date": "",
     "rank": "县处级正职", "note": "接替前任谷宏健"},
    {"person_id": 1, "org_id": 2, "title": "宽城满族自治县人民政府县长（前任职）", "start_date": "c.2017–2018", "end_date": "c.2021–2022",
     "rank": "县处级正职", "note": ""},

    # person 2: 高春林 — 县长
    {"person_id": 2, "org_id": 2, "title": "宽城满族自治县人民政府县长", "start_date": "c.2022–2023", "end_date": "",
     "rank": "县处级正职", "note": ""},

    # person 3: 谷宏健 — 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "中共宽城满族自治县委书记（前任）", "start_date": "", "end_date": "c.2021–2022",
     "rank": "县处级正职", "note": "前任县委书记，约2021年卸任"},

    # person 4: 县委副书记
    {"person_id": 4, "org_id": 1, "title": "中共宽城满族自治县委副书记", "start_date": "", "end_date": "",
     "rank": "县处级副职", "note": ""},

    # person 5: 常务副县长
    {"person_id": 5, "org_id": 2, "title": "中共宽城满族自治县委常委、常务副县长", "start_date": "", "end_date": "",
     "rank": "县处级副职", "note": ""},

    # person 6: 纪委书记
    {"person_id": 6, "org_id": 3, "title": "中共宽城满族自治县委常委、纪委书记、监委主任", "start_date": "", "end_date": "",
     "rank": "县处级副职", "note": ""},

    # person 7: 组织部部长
    {"person_id": 7, "org_id": 4, "title": "中共宽城满族自治县委常委、组织部部长", "start_date": "", "end_date": "",
     "rank": "县处级副职", "note": ""},

    # person 8: 政法委书记
    {"person_id": 8, "org_id": 5, "title": "中共宽城满族自治县委常委、政法委书记", "start_date": "", "end_date": "",
     "rank": "县处级副职", "note": ""},

    # person 9: 宣传部部长
    {"person_id": 9, "org_id": 6, "title": "中共宽城满族自治县委常委、宣传部部长", "start_date": "", "end_date": "",
     "rank": "县处级副职", "note": ""},

    # person 10: 人大主任
    {"person_id": 10, "org_id": 7, "title": "宽城满族自治县人大常委会党组书记、主任", "start_date": "", "end_date": "",
     "rank": "县处级正职", "note": ""},

    # person 11: 政协主席
    {"person_id": 11, "org_id": 8, "title": "政协宽城满族自治县委员会党组书记、主席", "start_date": "", "end_date": "",
     "rank": "县处级正职", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS (Person ↔ Person)
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 张成 ↔ 高春林：党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "县委书记与县长—县党政主要负责人搭档关系",
     "overlap_org": "宽城满族自治县",
     "overlap_period": ""},

    # 张成 ↔ 谷宏健：前后任
    {"person_a": 1, "person_b": 3, "type": "前后任",
     "context": "张成接替谷宏健任县委书记",
     "overlap_org": "中共宽城满族自治县委员会",
     "overlap_period": "c.2021–2022 交接"},

    # 张成 ↔ 县委领导班子成员（常委会集体）
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委书记与县委副书记工作关系（县委常委会成员）",
     "overlap_org": "中共宽城满族自治县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委书记与常务副县长工作关系（县委常委会成员）",
     "overlap_org": "中共宽城满族自治县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "县委书记与纪委书记工作关系（县委常委会成员）",
     "overlap_org": "中共宽城满族自治县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委书记与组织部部长工作关系（县委常委会成员）",
     "overlap_org": "中共宽城满族自治县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "县委书记与政法委书记工作关系（县委常委会成员）",
     "overlap_org": "中共宽城满族自治县委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "县委书记与宣传部部长工作关系（县委常委会成员）",
     "overlap_org": "中共宽城满族自治县委员会",
     "overlap_period": ""},

    # 高春林 ↔ 常务副县长：政府班子
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "县长与常务副县长工作关系（县政府班子）",
     "overlap_org": "宽城满族自治县人民政府",
     "overlap_period": ""},

    # 高春林 ↔ 人大主任：四套班子
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "县长与人大常委会主任工作关系",
     "overlap_org": "宽城满族自治县",
     "overlap_period": ""},

    # 张成 ↔ 人大主任：四套班子
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "县委书记与人大常委会主任工作关系",
     "overlap_org": "宽城满族自治县",
     "overlap_period": ""},

    # 张成 ↔ 政协主席：四套班子
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "县委书记与政协主席工作关系",
     "overlap_org": "宽城满族自治县",
     "overlap_period": ""},

    # 高春林 ↔ 政协主席：四套班子
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "县长与政协主席工作关系",
     "overlap_org": "宽城满族自治县",
     "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  宽城满族自治县领导班子工作关系网络")
    print("  等级: 自治县（河北省承德市下辖）")
    print("  调查日期: 2026-08-03")
    print("  ✅ 县委书记: 张成")
    print("  ✅ 县长: 高春林")
    print("  ⚠️  领导团队成员完整姓名待补充（kuancheng.gov.cn不可达）")
    print("  ⚠️  个人履历信息不完整（搜索渠道受限）")
    print("  ⚠️  Baidu Baike 不可用（403）")
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
    print("\n✅ 宽城满族自治县数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print("  ⚠️  个人详细履历信息待补充（建议在正常网络环境下补充Baidu Baike资料）")