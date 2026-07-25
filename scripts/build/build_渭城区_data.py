#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 渭城区, 咸阳市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_渭城区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.weicheng.gov.cn — 渭城区人民政府官方网站 (timeout during access attempt, July 2026)
  - www.xianyang.gov.cn — 咸阳市人民政府官方网站 (accessible, no 渭城区-specific leadership pages found)
  - News articles referencing 渭城区 leadership from government news feeds

Confidence notes:
  - Web access was heavily degraded during investigation: Exa rate-limited, Baidu 403, government site timeout
  - Current 区委书记 and 区长 identities are NOT confirmed from primary sources
  - Organizational structure is based on standard 市辖区 model (parallel to 灞桥区 template)
  - Person data fields marked 'unknown' represent confirmed gaps in available evidence
  - All claims labeled with confidence level; gaps explicitly documented in open_questions
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
for parent_count in [2, 3, 4, 5]:
    candidate = os.path.abspath(os.path.join(BASE, *[".."] * parent_count))
    if os.path.isdir(os.path.join(candidate, "gov_relation")):
        PROJECT_ROOT = candidate
        break
else:
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "渭城区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

# NOTE: Current 区委书记 and 区长 identities are unconfirmed due to web access
# limitations. Person IDs 1-2 are placeholders. Names should be replaced once
# confirmed via official sources (www.weicheng.gov.cn/zwgk/ldzc/).

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (区委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 区委书记 — 未确认（需要查询渭城区政府官网领导之窗页面确认具体人选）
    {
        "id": 1,
        "name": "（区委书记—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共咸阳市渭城区委员会",
        "source": "尚未从公开来源确认具体人选；建议查看 www.weicheng.gov.cn 领导之窗",
        "confidence": "unverified"
    },
    # 区长 — 未确认
    {
        "id": 2,
        "name": "（区长—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "咸阳市渭城区人民政府",
        "source": "尚未从公开来源确认具体人选；建议查看 www.weicheng.gov.cn 领导之窗",
        "confidence": "unverified"
    },
    # 区委副书记（专职）— 待确认
    {
        "id": 3,
        "name": "（区委副书记—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共咸阳市渭城区委员会",
        "source": "尚未从公开来源确认",
        "confidence": "unverified"
    },
    # 区委常委、区纪委书记、区监委主任 — 待确认
    {
        "id": 4,
        "name": "（纪委书记—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共咸阳市渭城区纪律检查委员会",
        "source": "尚未从公开来源确认",
        "confidence": "unverified"
    },
    # 区委常委、组织部部长 — 待确认
    {
        "id": 5,
        "name": "（组织部长—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共咸阳市渭城区委员会",
        "source": "尚未从公开来源确认",
        "confidence": "unverified"
    },
    # 区委常委、宣传部部长 — 待确认
    {
        "id": 6,
        "name": "（宣传部长—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共咸阳市渭城区委员会",
        "source": "尚未从公开来源确认",
        "confidence": "unverified"
    },
    # 区委常委、常务副区长 — 待确认
    {
        "id": 7,
        "name": "（常务副区长—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "咸阳市渭城区人民政府",
        "source": "尚未从公开来源确认",
        "confidence": "unverified"
    },
    # 区委政法委书记 — 待确认
    {
        "id": 8,
        "name": "（政法委书记—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共咸阳市渭城区委员会",
        "source": "尚未从公开来源确认",
        "confidence": "unverified"
    },
    # 区人大常委会主任 — 待确认
    {
        "id": 9,
        "name": "（人大常委会主任—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "咸阳市渭城区人民代表大会常务委员会",
        "source": "尚未从公开来源确认",
        "confidence": "unverified"
    },
    # 区政协主席 — 待确认
    {
        "id": 10,
        "name": "（政协主席—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议咸阳市渭城区委员会",
        "source": "尚未从公开来源确认",
        "confidence": "unverified"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共咸阳市渭城区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共咸阳市委员会",
        "location": "咸阳市渭城区"
    },
    {
        "id": 2,
        "name": "咸阳市渭城区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "咸阳市人民政府",
        "location": "咸阳市渭城区"
    },
    {
        "id": 3,
        "name": "咸阳市渭城区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "咸阳市人民代表大会常务委员会",
        "location": "咸阳市渭城区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议咸阳市渭城区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协咸阳市委员会",
        "location": "咸阳市渭城区"
    },
    {
        "id": 5,
        "name": "中共咸阳市渭城区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共咸阳市纪律检查委员会",
        "location": "咸阳市渭城区"
    },
]

positions_data = [
    # 区委
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "未确认具体人选"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "未确认具体人选"},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "未确认"},
    {"person_id": 4, "org_id": 5, "title": "区委常委、区纪委书记、区监委主任", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "未确认"},
    {"person_id": 5, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "未确认"},
    {"person_id": 6, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "未确认"},
    {"person_id": 7, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "未确认"},
    {"person_id": 8, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "未确认"},
    # 人大、政协
    {"person_id": 9, "org_id": 3, "title": "区人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "未确认"},
    {"person_id": 10, "org_id": 4, "title": "区政协主席", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "未确认"},
]

relationships_data = [
    # 基础组织关系 — 所有人员因在同一区委/政府工作而产生的基本共事关系
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长（党政一把手）工作关系", "overlap_org": "中共咸阳市渭城区委员会", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 3, "type": "工作关系", "context": "区委书记与专职副书记工作关系", "overlap_org": "中共咸阳市渭城区委员会", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 7, "type": "工作关系", "context": "区长与常务副区长工作关系", "overlap_org": "咸阳市渭城区人民政府", "overlap_period": "unknown-present"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(data: dict, filename: str) -> Path:
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")
    return path

def main():
    print(f"Building network for {SLUG}...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print()

    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  {len(persons_data)} persons")
    print(f"  {len(organizations_data)} organizations")
    print(f"  {len(positions_data)} positions")
    print(f"  {len(relationships_data)} relationships")
    print()
    print("  ⚠ NOTE: All person names are placeholders (unconfirmed).")
    print("    To fill in real names and biographies:")
    print("    1. Visit https://www.weicheng.gov.cn/zwgk/ldzc/")
    print("    2. Or search xianyang.gov.cn news for 渭城区 leadership mentions")
    print("    3. Update persons_data with confirmed names")
    print("    4. Create data/persons/YYYYMMDD-...json for each key figure")
    print("=" * 60)

if __name__ == "__main__":
    main()
