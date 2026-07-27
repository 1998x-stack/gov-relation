#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 惠农区 (Huinong District), 石嘴山市, 宁夏回族自治区.

Level: 市辖区
Province: 宁夏回族自治区
Parent city: 石嘴山市
Targets: 区委书记 (Party Secretary), 区长 (District Mayor)
Task ID: ningxia_惠农区

Research date: 2026-07-25
Official source: https://www.huinong.gov.cn/ (石嘴山市惠农区人民政府)

Current status (as of 2026-07-25, verified via huinong.gov.cn homepage):
- 区长: 马仲武 (confirmed — named in 惠农区五届人民政府第119次常务会议, 2026-06-23)
- 副区长: 张士海 (confirmed — presided over 第119次常务会议 on behalf of 区长)
- 区委书记: name 待确认 — not found in publicly accessible web sources during this investigation
- Full leadership roster: not fully extracted due to JS-dependent government CMS and degraded web search

Research limitations:
- Exa search API: rate-limited
- Baidu Baike: 403 blocked
- Jina Reader: timed out
- Government website (huinong.gov.cn): accessible at homepage level, but article detail pages are
  loaded dynamically via JavaScript, making direct URL access impossible
- Only the homepage text snippets were readable, revealing 马仲武 (区长) and 张士海 (副区长)

Known appointment documents listed on the site (content not accessible):
- 惠农区人民政府关于马芳等同志职务任免的通知 (2026-06-26)
- 惠农区人民政府关于郎强等同志职务任免的通知 (2026-05-07)
- 惠农区人民政府关于调整区人民政府区长 副区长工作分工的通知 (惠政办发〔2026〕20号, 2026-06-01)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "惠农区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 区委书记 — name unconfirmed
    {
        "id": 1,
        "name": "待确认-区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共惠农区委员会",
        "source": "Not confirmed from publicly accessible web sources as of 2026-07-25.",
    },

    # 2. 马仲武 — 区长 (District Mayor)
    {
        "id": 2,
        "name": "马仲武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "惠农区人民政府",
        "source": "Confirmed from 惠农区五届人民政府第119次常务会议 news on huinong.gov.cn (2026-06-23): '受马仲武区长委托，张士海副区长主持会议'",
    },

    # 3. 张士海 — 副区长 (Deputy Mayor)
    {
        "id": 3,
        "name": "张士海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "惠农区人民政府",
        "source": "Confirmed from 惠农区五届人民政府第119次常务会议 news on huinong.gov.cn (2026-06-23): '受马仲武区长委托，张士海副区长主持会议'",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共惠农区委员会", "type": "党委", "level": "县处级", "parent": "中共石嘴山市委员会", "location": "惠农区"},
    {"id": 2, "name": "惠农区人民政府", "type": "政府", "level": "县处级", "parent": "石嘴山市人民政府", "location": "惠农区"},
    {"id": 3, "name": "石嘴山市", "type": "政府", "level": "地市级", "parent": "宁夏回族自治区", "location": "石嘴山市"},
    {"id": 4, "name": "中共石嘴山市委员会", "type": "党委", "level": "地市级", "parent": "中共宁夏回族自治区委员会", "location": "石嘴山市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共惠农区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "区委书记姓名待确认"},
    # 马仲武 — 区长
    {"person_id": 2, "org_id": 2, "title": "惠农区区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "马仲武，2026年6月仍以区长身份参加政府常务会议"},
    # 张士海 — 副区长
    {"person_id": 3, "org_id": 2, "title": "惠农区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "张士海，2026年6月受马仲武区长委托主持召开常务会议"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长是惠农区党政正职关系", "overlap_org": "惠农区", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长与副区长是正副职关系", "overlap_org": "惠农区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与副区长", "overlap_org": "惠农区", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print(f"Building {SLUG} network...")

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

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
